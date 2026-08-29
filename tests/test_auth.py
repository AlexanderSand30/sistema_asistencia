import unittest

from app import app


class AuthRequiredRoutesTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_routes_require_login(self):
        protected_routes = [
            "/asistencia",
            "/trabajadores",
            "/reportes",
            "/produccion",
            "/perfil",
            "/usuarios/",
            "/api/asistencias",
            "/api/trabajadores",
            "/api/reportes",
            "/api/produccion",
        ]

        for path in protected_routes:
            with self.subTest(path=path):
                response = self.client.get(path, follow_redirects=False)
                self.assertIn(
                    response.status_code,
                    (302, 401, 403),
                    msg=f"Ruta {path} debería requerir inicio de sesión",
                )


if __name__ == "__main__":
    unittest.main()
