"""Automated unit and integration tests for cultural_spaces (HTTP calls mocked)."""
from unittest.mock import MagicMock, patch
from django.test import SimpleTestCase
from django.urls import reverse
import requests

from . import services


class CulturalSpacesTests(SimpleTestCase):
    """Test suite covering the 4 mandatory scenarios plus SoQL sanitization and CSV fallback."""

    def _mock_response(self, json_payload: list[dict]) -> MagicMock:
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = json_payload
        return mock_resp

    @patch("cultural_spaces.services.requests.get")
    def test_normal_search_renders_matching_spaces_and_summary(
        self, mock_get: MagicMock
    ) -> None:
        """Case 1 (Normal search): returns matching spaces, summary indicators, and source attribution."""
        mock_get.return_value = self._mock_response(
            [
                {
                    "tipo_lugar": "Biblioteca",
                    "divipola": "05001",
                    "departamento": "Antioquia",
                    "municipio": "Medellín",
                    "nombre_del_lugar": "BIBLIOTECA PUBLICA PILOTO DE MEDELLIN",
                    "descripci_n": "Biblioteca Pública registrada en RNBP",
                    "direcci_n_f_sica": "CARRERA 64 # 50 - 32",
                    "fuente": "Red Nacional de Bibliotecas Públicas",
                },
                {
                    "tipo_lugar": "Museo / Entidad Museal",
                    "divipola": "05001",
                    "departamento": "Antioquia",
                    "municipio": "Medellín",
                    "nombre_del_lugar": "MUSEO DE ANTIOQUIA",
                    "descripci_n": "Entidad museal registrada en SIMCO",
                    "direcci_n_f_sica": "CARRERA 52 # 52 - 43",
                    "fuente": "SIMCO",
                },
            ]
        )

        response = self.client.get(
            reverse("cultural_spaces:index"),
            {"departamento": "Antioquia", "municipio": "Medellín"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BIBLIOTECA PUBLICA PILOTO DE MEDELLIN")
        self.assertContains(response, "MUSEO DE ANTIOQUIA")
        self.assertContains(response, "Ministerio de las Culturas, las Artes y los Saberes")
        self.assertContains(response, "te39-v28f")
        self.assertEqual(response.context["summary"]["total_count"], 2)
        self.assertEqual(response.context["summary"]["unique_municipalities"], 1)

    @patch("cultural_spaces.services.requests.get")
    def test_no_matches_renders_clear_empty_message(
        self, mock_get: MagicMock
    ) -> None:
        """Case 2 (No matches): displays a clear Spanish message when search returns zero records."""
        mock_get.return_value = self._mock_response([])

        response = self.client.get(
            reverse("cultural_spaces:index"),
            {"q": "TerminoInexistenteXYZ999"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "No se encontraron espacios culturales que coincidan con los criterios de búsqueda",
        )
        self.assertEqual(response.context["summary"]["total_count"], 0)
        self.assertEqual(response.context["spaces"], [])

    @patch("cultural_spaces.services.requests.get")
    def test_empty_input_submission_has_defined_behavior(
        self, mock_get: MagicMock
    ) -> None:
        """Case 3 (Empty input): submitting blank/whitespace filters shows general results and notice."""
        mock_get.return_value = self._mock_response(
            [
                {
                    "tipo_lugar": "Casa de Cultura",
                    "departamento": "Cundinamarca",
                    "municipio": "Chía",
                    "nombre_del_lugar": "CASA DE LA CULTURA DE CHIA",
                    "descripci_n": "Casa de la Cultura municipal",
                    "direcci_n_f_sica": "CALLE 11 # 11 - 29",
                    "fuente": "SIlep",
                }
            ]
        )

        response = self.client.get(
            reverse("cultural_spaces:index"),
            {"q": "   ", "municipio": "", "departamento": "", "tipo_lugar": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["empty_search_submitted"])
        self.assertFalse(response.context["has_active_filters"])
        self.assertContains(
            response,
            "Mostrando el listado general de espacios culturales (no se ingresaron filtros de búsqueda).",
        )
        self.assertContains(response, "CASA DE LA CULTURA DE CHIA")
        called_params = mock_get.call_args.kwargs["params"]
        self.assertNotIn("$where", called_params)

    @patch("cultural_spaces.services.requests.get")
    def test_incomplete_record_does_not_break_interface(
        self, mock_get: MagicMock
    ) -> None:
        """Case 4 (Incomplete data): missing, None, or 'Sin Dato' fields use safe defaults without crashing."""
        mock_get.return_value = self._mock_response(
            [
                {
                    "nombre_del_lugar": None,
                    "tipo_lugar": "",
                    "departamento": "Sin Dato",
                    "municipio": None,
                    # direcci_n_f_sica, descripci_n, and fuente omitted completely
                }
            ]
        )

        response = self.client.get(reverse("cultural_spaces:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nombre no disponible")
        self.assertContains(response, "Sin clasificar")
        self.assertContains(response, "No especificada")
        self.assertContains(response, "Sin descripción disponible")
        self.assertContains(response, "No registrada")

    def test_soql_where_sanitizes_single_quotes_and_injection(self) -> None:
        """Verify user input single quotes are escaped before building $where."""
        malicious_input = "Teatro O'Higgins' OR '1'='1"
        where_clause = services.build_soql_where(query=malicious_input)
        self.assertIn("Teatro O''Higgins'' OR ''1''=''1", where_clause)
        self.assertEqual(
            where_clause,
            "upper(nombre_del_lugar) like upper('%Teatro O''Higgins'' OR ''1''=''1%')",
        )

    @patch("cultural_spaces.services.requests.get")
    def test_api_failure_falls_back_to_local_csv(
        self, mock_get: MagicMock
    ) -> None:
        """Verify network errors fall back gracefully to /data/cultural_spaces_sample.csv."""
        mock_get.side_effect = requests.ConnectionError("Simulated network outage")

        response = self.client.get(reverse("cultural_spaces:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["using_fallback"])
        self.assertGreater(len(response.context["spaces"]), 0)
        self.assertContains(response, "Aviso de conexión:")
