FROM python:3.11-slim-bullseye AS base

    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED=1 \
    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app" \
    POETRY_HOME="/opt/poetry" \
    APP_PATH="/app" \
    VENV_PATH="/app/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# build-base is used to build dependencies
FROM base as build

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Installing poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Configuring poetry
RUN poetry config virtualenvs.create true && poetry config virtualenvs.in-project true

# Copying requirements of a project
COPY pyproject.toml poetry.lock ${APP_PATH}/
WORKDIR ${APP_PATH}/

RUN --mount=type=cache,target=/root/.cache/pypoetry/cache \
    --mount=type=cache,target=/root/.cache/pypoetry/artifacts \
    poetry install -v --no-root --without dev

FROM build as build-dev

RUN --mount=type=cache,target=/root/.cache/pypoetry/cache \
    --mount=type=cache,target=/root/.cache/pypoetry/artifacts \
    poetry install -v --no-root

FROM base as development

# Copying poetry and venv into image
COPY --from=build-dev $POETRY_HOME $POETRY_HOME
COPY --from=build-dev $APP_PATH $APP_PATH

WORKDIR ${APP_PATH}/
COPY . .
# Instll only application package
RUN poetry install -v --only-root

CMD ["./worker.sh"]

FROM base as production

# Add a non-root user
RUN groupadd -rg 1000 appgroup \
    && useradd -rMg appgroup -s /usr/sbin/nologin -u 999 appuser

USER 999

# Copying poetry and venv into image
COPY --from=build --chown=appuser $POETRY_HOME $POETRY_HOME
COPY --from=build --chown=appuser $APP_PATH $APP_PATH

WORKDIR ${APP_PATH}/
COPY --chown=appuser . .
# Instll only application package
RUN poetry install --no-cache -v --only-root

# Remove unnedeed files
USER 0
RUN rm -rf $POETRY_HOME poetry.lock pyproject.toml
USER 999

CMD ["./worker.sh"]
