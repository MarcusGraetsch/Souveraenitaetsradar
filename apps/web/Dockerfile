# syntax=docker/dockerfile:1.7
FROM node:22-alpine AS build
WORKDIR /app
COPY apps/web/package*.json ./
RUN --mount=type=secret,id=build_ca_bundle \
    set -eu; \
    if [ -s /run/secrets/build_ca_bundle ]; then \
      NODE_EXTRA_CA_CERTS=/run/secrets/build_ca_bundle \
      npm_config_cafile=/run/secrets/build_ca_bundle \
        npm install --no-audit --no-fund; \
    else \
      npm install --no-audit --no-fund; \
    fi
COPY apps/web ./
RUN npm run build

FROM nginx:alpine
COPY apps/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
