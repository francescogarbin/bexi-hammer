# BluCRM BEXi Hammer

BEXi Hammer semplifica i test di chiamata a BluCRM BEXiAdapter con un ambiente grafico che mostra chiaramente le richieste disponibili e ne permette l'esecuzione in pochi clic del mouse.   

![bexi-hammer-screenshot-1](https://user-images.githubusercontent.com/571018/125612831-0824307c-7b8b-45b2-b0e8-1a90d058d7ab.png)

La lista delle richieste, sulla sinitra, riporta l'elenco dei file di richiesta disponibili per l'endpoint selezionato nella combo box. Il pannello di destra, chiamato Log, riporta il tracciato JSON della richiesta attualmente selezionata con sintax-highlight per facilitarne la lettura.

Puoi lanciare la richiesta selezionata nella lista richieste con un clic sul pulsante Esegui... nella toolbar. Il Log ti aggiornerà con tutti i progressi della chiamata al servizio BluCRM BEXi previsto dalla richiesta.

BEXi Hammer è un'applicazione multi-threading e può lanciare più richieste contemporaneamente. Lancia la seconda richiesta mentre la prima è in esecuzione e così via.

### Gli Endpoint

Abbiamo in previsione di fornire un riquadro di dialogo per la configurazione degli endpoint, per ora tuttavia vorrai editare il file di configurazione che trovi in una directory sul tuo sistema operativo.

Su Linux, trovi il file di configurazione a questo percorso:

<pre><code>/home/tuo_utente/.local/config/bexihammer</code></pre>

Il file di configurazione è in formato JSON e può ospitare una collection di endpoint. Apri il file di configurazione per trovare un esempio "dummy" di un endpoint. Rispettando la sintassi, puoi aggiungerne quanti ne vuoi.

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
  <li>Crea nuovi file con button "Nuovo" e editing con sintassi JSON evidenziata</li>
</ul>
