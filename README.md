# ![bexi-hammer-48x48](https://user-images.githubusercontent.com/571018/125659123-f532ccdd-c098-41ea-b6d5-fc7bd393fbc7.png) BluCRM BEXi Hammer

BEXi Hammer semplifica i test di chiamata a BluCRM BEXiAdapter con un ambiente grafico che mostra chiaramente le richieste disponibili e ne permette l'esecuzione in pochi clic del mouse.   

![bexi-hammer-1 3-20210805](https://user-images.githubusercontent.com/571018/128317035-bad33848-7370-4cbd-8da6-f8b8a33d8fe1.png)

La lista delle richieste, sulla sinistra, riporta l'elenco dei file di richiesta disponibili per l'ambiente BEXi selezionato nella combo box <i>Ambiente</i>. Il pannello di destra, Log Richiesta, riporta il tracciato JSON della richiesta attualmente selezionata; la sintassi è evidenziata per facilitare la lettura del tracciato.

Puoi lanciare la richiesta selezionata nella lista richieste con un clic sul pulsante <i>Esegui...</i> nella toolbar. Il Log ti aggiornerà con tutti i progressi della chiamata al servizio BluCRM BEXi previsto dalla richiesta.

BEXi Hammer è un'applicazione multi-threading: può lanciare e tracciare più richieste contemporaneamente. Lancia la seconda richiesta mentre la prima è in esecuzione e così via.

### Ambienti e endpoint BEXi

Un ambiente BEXi è puntato da uno URL radice (root URL) che punta ad uno o più server su cui risiedono i servizi di autenticazione e di esecuzione delle richieste. Una volta configurati un po' di ambienti, puoi selezionare l'ambiente corrente nella combo box Ambiente sopra il pannello Lista Richieste, BEXi Hammer caricherà automaticamente tutte le richieste disponibili per l'ambiente selezionato. 

In questa versione di BEXi Hammer, gli ambienti e gli endpoint sono configurati in un file di impostazioni. Ho in previsione di fornire un riquadro di dialogo per la configurazione degli endpoint, per ora tuttavia vorrai editare il file di configurazione che trovi in una directory sul tuo sistema operativo.

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
            ,"server_url":"https://www.altrodominio.com:1234"
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

Il file di configurazione è in formato JSON e può ospitare una collection di endpoint. Nell'esempio sopra ne trovi inseriti un paio. BluCRM ti comunicherà tutte le coordinata necessarie degli endpoint e le relative credenziali da impostare nella sezione <code>credentials</code>.

Apri il file di configurazione per trovare un esempio "dummy" di un endpoint, rispettando la sintassi, sopra esemplificata, puoi aggiungerne quanti ne vuoi.

### Aggiungere file di richiesta

Nel file di configurazione degli endpoint trovi il campo <pre><code>requests_files_path</code></pre> il cui valore punta ad una directory presente sul tuo file system.

Copia i file di richiesta all'interno di quella directory per visualizzarli automaticamente nella lista richieste.

Puoi anche puntare <code>requests_files_path</code> ad una directory di rete o condivisa; BEXi Hammer leggerà i file dalla cartella di rete. Questa funzionalità è molto utile quando lavori in team con un analista o un tester che produce richieste per te. Oppure per mantenere in un unico posto l'interno portfolio di richieste utilizzabili da più persone nel tuo team.

Se, mentre usi l'applicazione, aggiungi nuove richieste alla directory puntata da <code>requests_files_path</code>, fai clic sul button <code>Aggiorna</code>, collocato alla base della lista richieste, per caricarle.

### Requisiti

BEXi Hammer è scritto in Python 3 ed è compatibile con tutte le distribuzioni Linux moderne, Microsoft Windows e Apple MacOS.
Per funzionare correttamente, richiede solamente che i seguenti pacchetti siano già installati : 
interprete Python versione 3.8+
pacchetto GtkSource versione 4.0+

### Avviamento da terminale

Portarsi nella directory principale dell'applicazione e lanciare il comando:

<pre><code>python3 bexi-hammer.py</code></pre>

### Integrazione in Gnome su Linux

E' possibile lanciare BEXi Hammber dal menu Applicazioni di Gnome installando il file datadir/bexi-hammer.desktop in /usr/share/applications. Il file .desktop va editato per inserire manualmente il percorso alla directory che contiene i file dell'applicazione.

In alternativa, è sempre possibile l'avviamento da terminale.

### Installazione su Microsoft Window

Windows non è il mio ambiente preferito, se hai voglia di contribuire al progetto, fatti avanti! 

### Installazione su Apple MacOS

Purtroppo non dispongo un Mac recente su cui compilare il pacchetto di installazione. Se vuoi dare una mano, fatti avanti :-) In attesa di volontari, ti consiglio di affidarti all'applicazione Terminale e lanciare BEXi Hammer con il comando che trovi qualche linea sopra.

### Licenza d'uso e modifiche al codice sorgente

BEXi Hammer è un'applicazione che ha funzioni dimostrative, il codice è rilasciato sotto licenza [GNU GENERAL PUBLIC LICENSE V3](https://www.gnu.org/licenses/gpl-3.0.html) per consentirti di modificare il codice a tuo piacimento.

### Disclaimer e clausole di utilizzo

BEXi Hammer non è un prodotto di BluCRM Srl e pertanto non gode di alcuna clausola di supporto ufficiale e manutenzione. BEXi Hammer è un applicazione sviluppata e rilasciata a unico ed esclusivo scopo dimostrativo.  BEXi Hammer è rilasciato senza alcuna garanzia di funzionamento e di future evoluzioni e manutenzioni.

### Roadmap di sviluppo

#### Versione 1.3 (DOING)

<ul>
    <li>Nuovo pannello di log della richiesta, ridimensionabile e scrollabile (DONE)</li> 
    <li>Riquadro di dialogo Informazioni (DONE)</li>
    <li>Crea nuove richieste JSON con button "Nuovo" (DONE)</li>
    <li>Riquadro di dialogo Impostazioni per impostare settings da GUI (DOING)</li>
    <li>Lancio richieste massivo, utile per test massivi automatizzati (TODO)</li>
    <li>Pacchetto di installazione Flatpak per Linux (TODO)</li>
</ul>

#### Versione 1.2 (DONE)

<ul>
    <li>Icona applicazione</li>
    <li>File .desktop per lancio da menu Applicazioni su Linux</li>
    <li>Ottimizzazione del codice multi-threading di lancio richieste</li>
    <li>Miglioramento delle note di avanzamento richiesta nel panello Log</li>
    <li>Acceleratori da tastiera per lancio rapido di richieste e ripristino</li>
</ul>

#### Versione 1.1 (DONE)

<ul>
    <li>Panello Log con evidenziazione sintassi JSON</li>
    <li>Lancio richieste non bloccanti su thread dedicati</li>
    <li>Aggiungi richieste da file system all'endpoint corrente</li>
    <li>Salva contenuto del pannello Log</li>
</ul>

#### Versione 1.0 (DONE)

<ul>
    <li>GUI GTK+: toolbar, pannello Lista Richieste, pannello Log, status bar</li>
    <li>Carica endpoints e richieste da settings</li>
    <li>Carica richieste da directory locale/remota</li>
    <li>Esegui richieste UI-blocking verso token e BEXI Adapter</li>
    <li>Consulta il log richieste nel pannello Log</li>
</ul>

### Get in touch!

BEXi Hammer è il risultato del lavoro di qualche weekend. Mi ha aiutato moltissimo a capire la logica delle chiamate BEXi e mi sono divertito nello scriverlo a beneficio dei team che interfacciano BEXi. Scrivimi a francescogarbin@gmail.com: mi farebbe piacere avere dei suggerimenti :-)
