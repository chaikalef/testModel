GUNICORN_PORT=5017
CURR_USER=${USER}
WORK_DIR=$(pwd)
APP_NAME=flaskApp
WORKER_NUMBER=2

SITE_PATH=/etc/nginx/sites-available/$(APP_NAME)
SERVICE_PATH=/etc/systemd/system/$(APP_NAME).service
SITE_BAK=another/$(APP_NAME).nginxConfig.bak
SERVICE_BAK=another/$(APP_NAME).service.bak

ifdef CONDA_PREFIX
	ENV_DIR=$(CONDA_PREFIX)
else
	ENV_DIR=$(VIRTUAL_ENV)
endif


guni: src/web/wsgi.py
	make _allow_port
	gunicorn --workers $(WORKER_NUMBER) --bind localhost:$(GUNICORN_PORT) src.web.wsgi:appInstance

status:
	systemctl -a | grep $(APP_NAME)
	systemctl status $(APP_NAME)

all:
	make service
	make site

clean:
	make service_rm
	make site_rm

site: $(SITE_BAK)
	cp $(SITE_BAK) $(SITE_PATH)
	bash -c '(echo location \/ { ; \
			echo "proxy_pass http://localhost:$(GUNICORN_PORT);" ;\
			echo \}\}) >> $(SITE_PATH)'
	ln -s $(SITE_PATH) /etc/nginx/sites-enabled
	nginx -t
	ufw allow 'Nginx Full'
	nginx -s reload

service: $(SERVICE_BAK)
	make _allow_port
	cp $(SERVICE_BAK) $(SERVICE_PATH)
	bash -c '(echo User=$(CURR_USER) ; \
			echo "ExecStart=$(ENV_DIR)/bin/gunicorn --workers $(WORKER_NUMBER) --bind localhost:$(GUNICORN_PORT) src.web.wsgi:appInstance" ; \
			echo WorkingDirectory=$(WORK_DIR)) >> $(SERVICE_PATH)'
	bash -c 'echo Environment=\"PATH=$(ENV_DIR)/bin\" >> $(SERVICE_PATH)'
	systemctl start $(APP_NAME)
	systemctl enable $(APP_NAME)

site_rm: $(SITE_PATH)
	rm $(SITE_PATH) /etc/nginx/sites-enabled/$(APP_NAME)
	nginx -s reload

service_rm: $(SERVICE_PATH)
	make _deny_port
	systemctl stop $(APP_NAME)
	systemctl disable $(APP_NAME)
	rm $(SERVICE_PATH)

_allow_port:
	ufw allow $(GUNICORN_PORT)

_deny_port:
	ufw deny $(GUNICORN_PORT)