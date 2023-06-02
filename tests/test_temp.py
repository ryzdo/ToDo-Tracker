from flask import url_for

from webapp.user.models import User


class TestRegistration:
    def test_registration_load(self, client, captured_templates):
        response = client.get(url_for("user.register"))
        assert response.status_code == 200

        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == "user/registration.html"

        assert "page_title" in context
        assert context["page_title"] == "Регистрация"

    def test_registration_post(self, client, app):
        response = client.post(
            "/user/process-reg",
            data={
                "username": "Test",
                "email": "test@test.com",
                "password": "testpassword",
                "password2": "testpassword",
            },
        )
        assert response.status_code == 302

        assert User.query.count() == 1
        assert User.query.first().email == "test@test.com"
