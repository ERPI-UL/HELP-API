# FormuTools

**Fiche descriptive**

IaaS ERPI / ENSGSI : **ERPI**  
Recherche / Pédagogie: **Recherche**  
DNS : **erpi-s-indico.erpi.site.univ-lorraine.fr**  
Reseau: **interne**
___

## Start
First copy the `.env.example` file to `.env` and change the passwords inside.


## Command 

```sh 
# start the project 
docker-compose up -d
```

```sh 
# stop the project & remove the associated images 
docker-compose down --rmi all
```