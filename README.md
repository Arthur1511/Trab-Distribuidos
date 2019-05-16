# Trabalho Final Sistemas Distribuidos

### Resumo
Este trabalho consiste no desenvolvimento de uma aplicação
cliente/servidor para um jogo da velha onde o clinte enfrentará
o computador.

Aqui se encontra o codigo referente ao cliente java.

### Como executar

Primeiramente, caso não tenha, instale o modulo Pyro4 
(link se encontra nas referencias). 

Com o modulo devidamente instalado utilize o comando 
"pyro4-ns -n ip_servidor", onde ip_servidor é o ip da máquina 
que irá executar o servidor, para iniciar o servidor de nomes 
do pyro.

* Após iniciar o servidor de nomes execute o arquivo _servidor.py_.
* Execute o _cliente.py_ para jogar
* Caso queira testar a intercomunicação entre aplicações desenvolvidas
em linguagens diferentes, existe uma versão do cliente em Java que
se encontra em: https://github.com/Arthur1511/Trab-Distribuidos-cliente-java
 
### Caracteristicas
* As escolhas do computador serão feitas pelo algoritmo Min-max 
* O servidor será implementado em Python
* O cliente será implementado em Java
* Para a comunicação será utlizada a biblioteca Pyro4 (Python) e 
Pyrolite (Java)

### Referências

* https://pyro4.readthedocs.io/en/stable/index.html
* https://pythonhosted.org/Pyro4/pyrolite.html
