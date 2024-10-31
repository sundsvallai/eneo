# Development

## Architecture of each feature

The architecture for each feature strives to look like this:

```
feature_x/
├── api/
│   ├── feature_x_models.py
│   ├── feature_x_assembler.py
│   └── feature_x_router.py
├── feature_x.py
├── feature_x_repo.py
├── feature_x_service.py
└── feature_x_factory.py
```

An example of this can be seen in the `Spaces` feature.

### Function of each module

#### feature_x.py

The main class, the main domain object. Domain logic pertaining to how the feature works should live here.

#### feature_x_repo.py

Dependency inversion of database dependency. Should input a `Feature_x` class (or an `id`) and return that same class.

#### feature_x_service.py

Responsible for connecting this domain object with other related ones.

#### feature_x_factory.py

Factory class. Creates the domain object.

#### feature_x_router.py

Specifies the endpoints.

#### feature_x_models.py

Definition of the API schema.

#### feature_x_assembler.py

Translates domain objects to the API schema, allowing for the schema to change without affecting the shape of the domain object.

### Dependency injection

We use a [dependency injection framework](https://python-dependency-injector.ets-labs.org/index.html) to handle dependency injection for us. This framework creates all the other necessary classes, and handles their inter-dependency. This is typically done in the router.

### Connecting it together

Add the router [in the main router](https://github.com/inooLabs/intric-release/blob/main/backend/src/instorage/server/routers/__init__.py) in order to connect the endpoints to the application.

### Final considerations

While this is what we are striving towards at the moment, this is always subject to change.

## Migrations

We use [alembic](https://alembic.sqlalchemy.org/en/latest/) for our database migrations.