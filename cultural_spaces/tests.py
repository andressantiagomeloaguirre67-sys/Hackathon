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
        self.assertContains(response, "Filtros aplicados sin coincidencias")
        self.assertContains(response, "<code>TerminoInexistenteXYZ999</code>", html=False)
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

    @patch("cultural_spaces.services.requests.get")
    def test_extended_placeholders_and_invalid_limit_are_handled_safely(
        self, mock_get: MagicMock
    ) -> None:
        """Verify extended placeholder strings ('Sin información', 'No registra') and out-of-range limits."""
        mock_get.return_value = self._mock_response(
            [
                {
                    "nombre_del_lugar": "Sin información",
                    "tipo_lugar": "No aplica",
                    "departamento": "No registra",
                    "municipio": "Sin informacion",
                    "direcci_n_f_sica": "No registra",
                    "descripci_n": "Sin información",
                    "fuente": "N/A",
                }
            ]
        )

        result = services.fetch_cultural_spaces(limit=-10)
        called_params = mock_get.call_args_list[0].kwargs["params"]
        self.assertEqual(called_params["$limit"], "1")
        self.assertEqual(result["items"][0]["name"], "Nombre no disponible")
        self.assertEqual(result["items"][0]["space_type"], "Sin clasificar")
        self.assertEqual(result["items"][0]["department"], "No especificado")
        self.assertEqual(result["items"][0]["address"], "No especificada")
        self.assertEqual(result["items"][0]["description"], "Sin descripción disponible")
        self.assertEqual(result["items"][0]["source"], "No registrada")

    def _make_records(self, amount: int) -> list[dict]:
        return [
            {
                "tipo_lugar": "Biblioteca",
                "departamento": "Antioquia",
                "municipio": f"Municipio {index}",
                "nombre_del_lugar": f"BIBLIOTECA {index:03d}",
            }
            for index in range(amount)
        ]

    @patch("cultural_spaces.services.requests.get")
    def test_summary_covers_all_matching_records_not_only_listed_page(
        self, mock_get: MagicMock
    ) -> None:
        """With a full page, grouped queries compute indicators over every matching record."""
        mock_get.side_effect = [
            self._mock_response(self._make_records(services.DEFAULT_LIMIT)),
            self._mock_response(
                [
                    {"tipo_lugar": "Biblioteca", "total": "1200"},
                    {"tipo_lugar": "Sitio Arqueológico", "total": "6000"},
                    {"tipo_lugar": "Casa de Cultura", "total": "358"},
                ]
            ),
            self._mock_response(
                [
                    {"departamento": "Antioquia", "municipio": "Medellín"},
                    {"departamento": "Antioquia", "municipio": "Envigado"},
                    {"departamento": "Antioquia", "municipio": "Sin Dato"},
                ]
            ),
        ]

        response = self.client.get(
            reverse("cultural_spaces:index"), {"departamento": "Antioquia"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_available"], 7558)
        self.assertTrue(response.context["summary_covers_all"])
        self.assertEqual(response.context["summary"]["unique_municipalities"], 2)
        self.assertEqual(response.context["summary"]["unique_departments"], 1)
        self.assertEqual(
            response.context["summary"]["top_types"][0],
            {"name": "Sitio Arqueológico", "count": 6000},
        )
        self.assertContains(response, "7.558")
        self.assertContains(response, "Se listan los primeros 40")
        self.assertContains(response, "Los indicadores de abajo se calculan sobre los 7.558 resultados")
        self.assertContains(response, "<strong>Sitio Arqueológico:</strong> 6.000", html=False)
        type_params = mock_get.call_args_list[1].kwargs["params"]
        self.assertEqual(type_params["$group"], "tipo_lugar")
        self.assertIn("upper(departamento) = upper('Antioquia')", type_params["$where"])
        place_params = mock_get.call_args_list[2].kwargs["params"]
        self.assertEqual(place_params["$group"], "departamento, municipio")

    @patch("cultural_spaces.services.requests.get")
    def test_aggregate_failure_falls_back_to_listed_page_and_count(
        self, mock_get: MagicMock
    ) -> None:
        """If grouped queries fail, indicators use the listed page and say so; count(*) still gives the total."""
        mock_get.side_effect = [
            self._mock_response(self._make_records(services.DEFAULT_LIMIT)),
            requests.Timeout("Simulated slow group query"),
            self._mock_response([{"total": "7558"}]),
        ]

        response = self.client.get(reverse("cultural_spaces:index"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["summary_covers_all"])
        self.assertEqual(response.context["total_available"], 7558)
        self.assertEqual(response.context["summary"]["total_count"], services.DEFAULT_LIMIT)
        self.assertContains(response, "se calculan solo sobre los 40 espacios listados")
        self.assertContains(response, "Municipios (listados)")

    @patch("cultural_spaces.services.requests.get")
    def test_all_extra_queries_failing_still_renders_listed_results(
        self, mock_get: MagicMock
    ) -> None:
        """If grouped and count queries all fail, the page still shows the records without a total."""
        mock_get.side_effect = [
            self._mock_response(self._make_records(services.DEFAULT_LIMIT)),
            requests.Timeout("Simulated slow group query"),
            requests.Timeout("Simulated slow count"),
        ]

        response = self.client.get(reverse("cultural_spaces:index"))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["total_available"])
        self.assertFalse(response.context["shows_partial_results"])
        self.assertEqual(len(response.context["spaces"]), services.DEFAULT_LIMIT)

    @patch("cultural_spaces.services.requests.get")
    def test_small_result_set_does_not_request_count(
        self, mock_get: MagicMock
    ) -> None:
        """With fewer records than the page limit, the total is known without a second query."""
        mock_get.return_value = self._mock_response(self._make_records(3))

        response = self.client.get(reverse("cultural_spaces:index"), {"q": "biblioteca"})

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(response.context["total_available"], 3)
        self.assertFalse(response.context["shows_partial_results"])

    @patch("cultural_spaces.services.requests.get")
    def test_fallback_explains_it_is_a_sample(self, mock_get: MagicMock) -> None:
        """Offline mode states that the data is a local sample and how big it is."""
        mock_get.side_effect = requests.ConnectionError("Simulated network outage")
        sample_size = services.count_fallback_records()

        response = self.client.get(reverse("cultural_spaces:index"))

        self.assertEqual(response.context["sample_size"], sample_size)
        self.assertContains(response, "muestra real de respaldo")
        self.assertContains(response, f"({sample_size} registros descargados de datos.gov.co")
        self.assertContains(response, "No representa el conjunto completo")
        self.assertEqual(response.context["total_available"], sample_size)
        self.assertEqual(response.context["summary"]["total_count"], sample_size)

    def test_fallback_results_are_sorted_by_name_like_the_api(self) -> None:
        """Offline results use the same alphabetical order as $order=nombre_del_lugar ASC."""
        records = [
            services.normalize_space_record({"nombre_del_lugar": name})
            for name in ["Teatro Colón", "archivo central", "Museo del Oro"]
        ]
        names = [item["name"] for item in services._filter_fallback_records(records)]
        self.assertEqual(names, ["archivo central", "Museo del Oro", "Teatro Colón"])
