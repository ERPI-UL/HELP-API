# étape de build
#FROM node:lts-alpine as build-stage
FROM node:lts-alpine
RUN npm install -g http-server
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 8080
CMD [ "http-server", "-P", "http://localhost:8080?", "dist" ]

# étape de production
#FROM nginx:stable-alpine as production-stage
#COPY --from=build-stage /app/dist /usr/share/nginx/html
#COPY ./nginx.conf /etc/nginx/conf.d/default.conf
#EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]