FROM node as builder
WORKDIR /app/
COPY . .
RUN npm install
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html/

# https://stackoverflow.com/questions/44438637/arg-substitution-in-run-command-not-working-for-dockerfile
ARG CODE_VERSION

RUN echo "This is (leaderboard) $CODE_VERSION"
RUN echo "This is (leaderboard) $CODE_VERSION" > /usr/share/nginx/html/VERSION

RUN chown -R nginx:nginx /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/conf.d/default.conf