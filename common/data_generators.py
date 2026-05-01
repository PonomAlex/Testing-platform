from faker import Faker

faker = Faker()


def random_post_payload() -> dict:
    return {
        "title": faker.sentence(nb_words=6),
        "body": faker.paragraph(nb_sentences=3),
        "userId": faker.random_int(min=1, max=10),
    }


def random_user_payload() -> dict:
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.unique.email(),
    }
