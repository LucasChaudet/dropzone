# Front DropZone : image multi-stage.
# 1) "build" : Node construit l'application (npm run build -> dist/) ;
# 2) l'image finale : nginx sans privilèges sert les fichiers statiques sur le port 8080.

FROM node:24-alpine AS build

WORKDIR /app

# Les dépendances d'abord : cette couche reste en cache tant que le lockfile ne change pas.
COPY package.json package-lock.json .npmrc ./
RUN npm ci

COPY . .

# Adresse de l'API vue par le navigateur, fixée au build (derrière nginx : /api).
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build


FROM nginxinc/nginx-unprivileged:1.29-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080

# nginx sert la page d'accueil (wget est fourni par l'image alpine).
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q --spider http://127.0.0.1:8080/ || exit 1
