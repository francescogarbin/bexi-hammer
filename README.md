# BluCRM BEXi Hammer

BEXi Hammer semplifica i test di chiamata a BluCRM BEXiAdapter con un ambiente grafico che mostra chiaramente le richieste disponibili e ne permette l'esecuzione in pochi clic del mouse.   

![bexi-hammer-screenshot-1](https://user-images.githubusercontent.com/571018/125612831-0824307c-7b8b-45b2-b0e8-1a90d058d7ab.png)

La lista delle richieste, sulla sinistra, riporta l'elenco dei file di richiesta disponibili per l'endpoint selezionato nella combo box. Il pannello di destra, chiamato Log, riporta il tracciato JSON della richiesta attualmente selezionata con sintax-highlight per facilitarne la lettura.

Puoi lanciare la richiesta selezionata nella lista richieste con un clic sul pulsante Esegui... nella toolbar. Il Log ti aggiornerà con tutti i progressi della chiamata al servizio BluCRM BEXi previsto dalla richiesta.

BEXi Hammer è un'applicazione multi-threading e può lanciare più richieste contemporaneamente. Lancia la seconda richiesta mentre la prima è in esecuzione e così via.

### Gli Endpoint

Ho in previsione di fornire un riquadro di dialogo per la configurazione degli endpoint, per ora tuttavia vorrai editare il file di configurazione che trovi in una directory sul tuo sistema operativo.

Su Linux, trovi il file di configurazione a questo percorso:

<pre><code>/home/tuo_utente/.config/bexihammer</code></pre>

La configurazione di un endpoint prevede pochi campi, eccoli nell'esempio sotto. Ricorda che trattandosi di un file JSON non sono ammessi commenti o istruzioni non previste dalla specifica ufficiale disponibile su www.json.org.

<pre><code>
{
    "version":"1.0"
    ,"endpoints":[
        {
            "identifier":"primo-endpoint"
            ,"visible_name":"Il mio primo endpoint"
            ,"requests_files_path":"/home/tuonome/richieste-del-primo-endpoint"
            ,"server_url":"https://primo.dominio.com"
            ,"token_route":"IBexAdapter/token"
            ,"adapter_route":"IBexAdapter/api/FrontOffice/startNewTask"
            ,"credentials": {
                "username":"il_mio_username"
                ,"password":"la_mia_password"
                ,"client_secret":"il_client_secret"
                ,"client_id":"il_client_id"
                ,"scope":"uno_scope"
                ,"grant_type":"un_grant_type"
            }
        }        
        ,{
            "identifier":"secondo-endpoint"
            ,"visible_name":"Il mio secondo endpoint"
            ,"requests_files_path":"/home/tuonome/secondo-endpoint-richieste"
            ,"server_url":"https://secondo.altrodominio.com"
            ,"token_route":"IBexAdapter/token"
            ,"adapter_route":"IBexAdapter/api/FrontOffice/startNewTask"
            ,"credentials": {
                "username":"il_mio_username"
                ,"password":"la_mia_password"
                ,"client_secret":"il_client_secret"
                ,"client_id":"il_client_id"
                ,"scope":"uno_scope"
                ,"grant_type":"un_grant_type"
            }
        }
    ]
}
</code></pre>

Il file di configurazione è in formato JSON e può ospitare una collection di endpoint. Nell'esempio sopra ne trovi inseriti un paio. BluCRM ti comunicherà tutte le coordinata necessarie degli endpoint e le relative credenziali.

Apri il file di configurazione per trovare un esempio "dummy" di un endpoint, rispettando la sintassi, sopra esemplificata, puoi aggiungerne quanti ne vuoi.

### Aggiungere file di richiesta

Nel file di configurazione degli endpoint trovi il campo <pre><code>requests_files_path</code></pre> il cui valore punta ad una directory presente sul tuo file system.

Copia i file di richiesta all'interno di quella directory per visualizzarli automaticamente nella lista richieste.

Puoi anche puntare ad una directory di rete o condivisa, BEXi Hammer leggerà i file dalla cartella di rete: questa funzionalità è molto utile quando lavori in team con un analista o un tester che produce richieste per te. Oppure per mantenere in un unico posto l'interno portfolio di richieste utilizzabili da più persone nel tuo team.

Se, mentre usi l'applicazione, aggiungi nuove richieste alla directory puntata da <code>requests_files_path</code>, fai clic sul button <code>Aggiorna</code>, collocato alla base della lista richieste, per caricarle.

### Requisiti

BEXi Hammer è scritto in Python 3 ed è compatibile con tutte le distribuzioni Linux moderne, Microsoft Windows e Apple MacOS.
Per funzionare correttamente, richiede solamente che i seguenti pacchetti siano già installati : 
interprete Python versione 3.8+
pacchetto GtkSource versione 4.0+

### Avviamento da terminale

Portarsi nella directory principale dell'applicazione e lanciare il comando:

<pre><code>python3 bexi-hammer.py</code></pre>

### BEXi Hammer integrazione Gnome su Linux

E' possibile lanciare BEXi Hammber dal menu Applicazioni di Gnome installando il file datadir/bexi-hammer.desktop in /usr/share/applications. Il file .desktop va editato per inserire manualmente il percorso alla directory che contiene i file dell'applicazione.

In alternativa, è sempre possibile l'avviamento da terminale.

### Installazione su Microsoft Window

Windows non è il mio ambiente preferito, se hai voglia di contribuire al progetto, fatti avanti! 

### Installazione su Apple MacOS

Purtroppo non dispongo un Mac recente su cui compilare il pacchetto di installazione. Se vuoi dare una mano, fatti avanti :-) In attesa di volontari, ti consiglio di affidarti all'applicazione Terminale e lanciare BEXi Hammer con il comando che trovi qualche linea sopra.

### Licenza d'uso e modifiche al codice sorgente

BEXi Hammer è un'applicazione che ha funzioni dimostrative, il codice è rilasciato sotto licenza GNU GENERAL PUBLIC LICENSE V3 per consentirti di modificare il codice a tuo piacimento.

### Roadmap di sviluppo

#### Versione 1.1a

<ul>
  <li>Dialogo Informazioni</li>
  <li>Dialogo Impostazioni</li>
  <li>Pacchetto di installazione FlatPack per sistemi Linux</li>
  <li>Crea nuovi file con button "Nuovo"</li>
</ul>

### Get in touch!

Per contatti e informazioni scrivimi a francescogarbin@gmail.com, mi farebbe piacere sare cosa pensi del progetto e se hai voglia di dare una mano.

