FROM prom/prometheus

COPY ./prometheus.yml ./etc/prometheus/prometheus.yml

EXPOSE 9090

WORKDIR /etc/prometheus/

ENTRYPOINT ["/bin/prometheus"]

CMD ["--config.file=prometheus.yml"]