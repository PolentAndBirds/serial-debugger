
// jte_interface.c

/*
protocollo TCM
tutti i comandi dal PC iniziano con #
comandi da 2 caratteri:
#: trasmette intestazione e tabelle
#. trasmette i dati della tabella
## blocca la trasmissione
#$ riprende la trasmissione
#R reset software

comandi da 3 caratteri:
#T1 trasmette la tabella numero 1 (nomi delle variabili), tabelle da 0 a 9
#P1 trasmette i dati del punto 1 (tabelle con punti), punti da 0 a 9
#+03 incrementa la variabile numero 3, numero variabile da 01 a 99 in ascii
#-04 decrementa la variabile numero 4
#*03 incrementa la variabile numero 3 2 volte
#/04 decrementa la variabile numero 4 2 volte



protocollo in trasmissione:

trasmetti versione
0xf2, nome macchina, versioni, 0xff

stringa debug
0xf4, stringa, 0xff

nomi tabelle
0xf3, indice tabella, nome, se ha i punti, 0xff
...

nomi variabili tabella
0xf0, indice della variabile, nome della variabile,  step, 0xff
...

valori variabili tabella
0xf1, indice, dimensione, variabile, 0xff
...








note d'uso per le tabelle:
step e' facoltativo, se non c'e', e' come se fosse a 0
step puo' essere un numero qualsiasi (tranne alcune eccezioni),
se il comando arriva 2 volte entro 1 secondo lo step viene moltiplicato per 10
se step_debug e' 101 la variabile spedita e' uno spazio vuoto e non viene visualizzato niente
se step_debug e' 99 viene spedito ON/OFF come se fosse un flag
se lo step e' 102 viene spedita una stringa di ram
se lo step e' 103 viene spedita una stringa di const (la variabile e' un puntatore)
se lo step e' 111 viene messo una virgola prima dell'ultima cifra (1 decimale)
se lo step e' 112 viene messo una virgola prima della penultima cifra (2 decimali)
la prima variabile e' solo un titolo e appare nel PC in grassetto,
il campo extra puo' definire una variabile con segno (viene trasmesso in testa + o -)

note d'uso per la tabella delle tabelle:
posso gestirne al massimo 9,
metti a 1 il primo parametro se vuoi gestire i punti
il secondo parametro impone dei vincoli alla tabella,
elenco restrizioni:
1: i dati di tabella sono modificabili solo se si imposta operatore=123
2: i dati di tabella sono modificabili solo se si imposta operatore=12
*/



#include "header.h"

#define tempo_per_doppio_click    1000

// tabella variabili, max 26 variabili per tabella
// ci sono varie tabelle che vengono caricate in funzione dei comandi provenienti dal PC

// le variabili visualizzate sono al massimo 50
#define max_variabili_debug     100

// struttur di ram
typedef struct tipo_struct_var_da_debuggare {
  char *nome_variabile;
  char *punta_variabile;
  char dimensione_variabile;
  char step;
  char type_var;
} var_da_debuggare;


//typedef struct tipo_struct_tabella_var {
//  char *nome_tabella;
//  var_da_debuggare *var_tabella;
//  char *con_punti;
//} tipo_tabella_var;


typedef struct tipo_struct_tabella_var {
  char *nome_tabella;
  var_da_debuggare *var_tabella;
  char with_points;
  char special;
} tipo_tabella_var;

unsigned char   titolo;     // variabile di appoggio per tabella

#define TABLE_WITH_POINTS							1

#define STEP_VOID                     101
#define STEP_DEBUG_MIG_PULSE          200
#define STEP_DEBUG_MIG_STD						201
#define STEP_DEBUG_CALIBRATION				202

#define TYPE_VAR_WITH_SIGN                 1
#define TYPE_VAR_WITH_1_DECIMAL            2
#define TYPE_VAR_WITH_2_DECIMALS           3
#define TYPE_VAR_WITH_SIGN_AND_1_DECIMAL   4
#define TYPE_VAR_WITH_SIGN_AND_2_DECIMALS  5
#define TYPE_VAR_STRING_RAM							 	 6
#define TYPE_VAR_STRING_CONST	  					 7
#define TYPE_VAR_ON_OFF                    8



unsigned char  trasmetti_nomi_tabelle;
unsigned char  trasmetti_valori_delle_variabili_tabella;
unsigned char  trasmetti_nomi_delle_variabili_tabella;

unsigned short timer_debug;
unsigned char  attendi_comando;
unsigned char  attendi_secondo_comando, secondo_comando;
unsigned char  blocca_trasmissione;
unsigned char  fase_debug, indice_debug;
unsigned char  input_debug;


#define timeout_uart  3000

unsigned char   punta_stringa_debug;

unsigned char   indice_tabella_var;
unsigned char   segno_da_trasmettere;
unsigned char   carat_debug[32], punta_carat_debug;
unsigned char   cambia_tabella;
unsigned char   indice_step, step_piu, step_meno;

unsigned long   var_debug;

unsigned char   trasmetti_versione_232;


/*
unsigned char
unsigned char
unsigned char
unsigned char
*/

#include "tab_jte_interface.h"

#define numero_tabelle_var  sizeof(tabella_var)/sizeof(tipo_tabella_var)




void invia_byte_uart(unsigned char);

void protocollo_jte(void);
void protocollo_diter(void);



//*******************************************************************
void run_jte_interface(void)
{
  if (attendi_comando) attendi_comando--;
  if (attendi_secondo_comando) attendi_secondo_comando--;

  if (pc_presente)
  {
    protocollo_jte();
    return;
  }

  if (punta_rx2!=punta_rx2_jte)
  {
    input_uart2=rx2[punta_rx2_jte];
    punta_rx2_jte++;
  }
  else
    input_uart2=0;

  input_debug=input_uart2;

  // se non ho ancora ricevuto niente mi aspetto un carattere di start
  if (input_debug)
  {
  	if (attendi_comando)
    {
      attendi_comando=0;
    
      if (input_debug==':')
      { // invio stringa di intestazione
      	pc_presente=1;
        trasmetti_versione_232=1;
        trasmetti_nomi_tabelle=1;
        timer_pc_presente=timeout_uart;
        timer_debug=0;
        fase_debug=0;
      }
    }
    else
    {
      if (input_debug=='#')
      {
      	attendi_comando=100;
      }
    }
    input_debug=0;
  }
}



void protocollo_jte(void)
{
  unsigned char char_debug;

  // timeout per il flag pc_presente
  if (timer_pc_presente)
    timer_pc_presente--;
  else
  {
    pc_presente=0;
    attendi_comando=0;
    attendi_secondo_comando=0;
    trasmetti_nomi_delle_variabili_tabella=0;
    trasmetti_valori_delle_variabili_tabella=0;
    trasmetti_versione_232=0;
    trasmetti_nomi_tabelle=0;
    fase_debug=0;
    indice_debug=0;
    cambia_tabella=0;
    timer_debug=0;
  }

  if (punta_rx2!=punta_rx2_jte)
  {
//
//if (rx2[punta_rx2_tcm]=='#');
//else if (rx2[punta_rx2_tcm]=='.');
//else
//{
//debug7++;
//debug8=debug9;
//debug9=debug10;
//debug10=rx2[punta_rx2_tcm];
//}
//
		input_uart2=rx2[punta_rx2_jte];
		punta_rx2_jte++;
  }
  else
    input_uart2=0;

  input_debug=input_uart2;

//  // la trasmissione dell astringa pu� essere lunga e nela frattempo il pc invia richieste che gvanno ignorate
//  if (trasmetti_stringa)
//  	input_debug=0;

  if (input_debug)
  {
    //pin_exp_12_on;

    if (attendi_secondo_comando)
    {
      attendi_secondo_comando=0;

      if (secondo_comando=='T')
      {
        if ((input_debug>='0')&&(input_debug<='9'))
        { // carico la tabella
          cambia_tabella=input_debug;
        }
      }
      else if (secondo_comando=='P')
      {
      }
      else if ((secondo_comando=='+')||
               (secondo_comando=='-')||
               (secondo_comando=='*')||
               (secondo_comando=='/'))
      { // ricevo l'indice in ascii in 2 step, 01..99
        if (!indice_step)
        {
          if ((input_debug>='0')&&(input_debug<='9'))
          {
            attendi_secondo_comando=100;
            indice_step=input_debug;
          }
        }
        else
        {
        	indice_step=indice_step-'0';
          indice_step=indice_step*10;
          if ((input_debug>='0')&&(input_debug<='9'))
          {
            indice_step=indice_step+(input_debug-'0');
            if (secondo_comando=='+')
            {
            	step_piu=1;
            }
            else if (secondo_comando=='-')
            {
            	step_meno=1;
            }
            else if (secondo_comando=='*')
            {
              step_piu=9;
            }
            else if (secondo_comando=='/')
            {
              step_meno=9;
            }
          }
        }
      }
    }
    else if (attendi_comando)
    {
      attendi_comando=0;
      blocca_trasmissione=0;

      if (input_debug=='#')
      {
        blocca_trasmissione=1;
      }
      else if (input_debug=='$')
      { //
        blocca_trasmissione=0;
      }
      else if (input_debug=='T')
      { // tabella
        attendi_secondo_comando=100;
        secondo_comando='T';
      }
      else if (input_debug=='P')
      { // punto
        attendi_secondo_comando=100;
        secondo_comando='P';
      }
      else if (input_debug=='+')
      { // incrementa
        attendi_secondo_comando=100;
        secondo_comando='+';
      }
      else if (input_debug=='-')
      { // decrementa
        attendi_secondo_comando=100;
        secondo_comando='-';
      }
      else if (input_debug=='*')
      { // doppio +
        attendi_secondo_comando=100;
        secondo_comando='*';
      }
      else if (input_debug=='/')
      { // doppio -
        attendi_secondo_comando=100;
        secondo_comando='/';
      }
      else if (input_debug=='.')
      { // invio i dati della tabella
      	if (!trasmetti_valori_delle_variabili_tabella)
      		trasmetti_valori_delle_variabili_tabella=1;
        timer_pc_presente=timeout_uart;
      }
      else if (input_debug=='R')
      { // reset software
        debug1=0;
        debug2=0;
        debug3=0;
        debug4=0;
        debug5=0;
        debug6=0;
        debug7=0;
        debug8=0;
        debug9=0;
        debug10=0;
      }
    }
    else if (input_debug=='#')
    {
      attendi_comando=100;
    }

    input_debug=0;


    if (step_meno)
    { // -
      unsigned short step_debug;
      unsigned char type_debug;

      step_debug=tabella_var[indice_tabella_var].var_tabella[indice_step].step;
      type_debug=tabella_var[indice_tabella_var].var_tabella[indice_step].type_var;

      if (step_debug==STEP_VOID) step_debug=0;
      else if (type_debug==TYPE_VAR_ON_OFF) step_debug=1;
      else step_debug=step_debug*step_meno;

      step_meno=0;

      if (tabella_var[indice_tabella_var].var_tabella[indice_step].dimensione_variabile==1)
      {
        if ((type_debug==TYPE_VAR_WITH_SIGN)||
            (type_debug==TYPE_VAR_WITH_SIGN_AND_1_DECIMAL))
        {
          if ((127+*tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile)>step_debug)
          {
            *tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile=*tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile-step_debug;
          }
          else
            *tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile=0;
        }
        else
        {
          if (*tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile>step_debug)
            *tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile=*tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile-step_debug;
          else
            *tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile=0;
        }
      }
      else if (tabella_var[indice_tabella_var].var_tabella[indice_step].dimensione_variabile==2)
      {
        unsigned short vvv;
        vvv=*tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile;
        vvv=vvv+(*(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+1))*256;
        if (vvv>step_debug)
          vvv=vvv-step_debug;
        else
          vvv=0;
        *tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile=vvv;
        vvv>>=8;
        *(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+1)=vvv;
      }
      else if (tabella_var[indice_tabella_var].var_tabella[indice_step].dimensione_variabile==4)
      {
        unsigned short vvv;
        vvv=*tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile;
        vvv=vvv+(*(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+1))*256;
        vvv=vvv+(*(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+2))*256*256;
        vvv=vvv+(*(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+3))*256*256*256;
        if (vvv>step_debug)
          vvv=vvv-step_debug;
        else
          vvv=0;
        *tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile=vvv;
        vvv>>=8;
        *(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+1)=vvv;
        vvv>>=8;
        *(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+2)=vvv;
        vvv>>=8;
        *(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+3)=vvv;
      }
      indice_step=0;
    }

    if (step_piu)
    { // +
      unsigned short step_debug;
      unsigned char type_debug;

      step_debug=tabella_var[indice_tabella_var].var_tabella[indice_step].step;
      type_debug=tabella_var[indice_tabella_var].var_tabella[indice_step].type_var;


      if (step_debug==STEP_VOID) step_debug=0;
      else if (type_debug==TYPE_VAR_ON_OFF) step_debug=1;
      else step_debug=step_debug*step_piu;

      step_piu=0;

      if (tabella_var[indice_tabella_var].var_tabella[indice_step].dimensione_variabile==1)
        *tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile=*tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+step_debug;
      else if (tabella_var[indice_tabella_var].var_tabella[indice_step].dimensione_variabile==2)
      {
        unsigned short vvv;
        vvv=*tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile;
        vvv=vvv+(*(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+1))*256;
        vvv=vvv+step_debug;
        *tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile=vvv;
        vvv>>=8;
        *(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+1)=vvv;
      }
      else if (tabella_var[indice_tabella_var].var_tabella[indice_step].dimensione_variabile==4)
      {
        unsigned short vvv;
        vvv=*tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile;
        vvv=vvv+(*(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+1))*256;
        vvv=vvv+(*(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+2))*256*256;
        vvv=vvv+(*(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+3))*256*256*256;
        vvv=vvv+step_debug;
        *tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile=vvv;
        vvv>>=8;
        *(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+1)=vvv;
        vvv>>=8;
        *(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+2)=vvv;
        vvv>>=8;
        *(tabella_var[indice_tabella_var].var_tabella[indice_step].punta_variabile+3)=vvv;
      }
      indice_step=0;
    }
  }
    //else
    //  pin_exp_12_off;


  // la sequenza delle trasmissioni deve essere questa:
  // nomi_tabelle, versione, nomi_variabili_tabelle, valori_tabelle (ricorsivo)
  if (blocca_trasmissione)
    return;

  if (trasmetti_versione_232)
  {
    if (fase_debug==0)
    {
      if (timer_debug>10)
      {
        invia_byte_uart(0xf2);
        fase_debug++;
        indice_debug=0;
        timer_debug=0;
      }
      else timer_debug++;
    }
    else if (fase_debug==1)
    {
      char_debug=*(machine_name+indice_debug);
      if (char_debug=='\0')
      { // fine nome, devo inviare la versione
        fase_debug=2;
        indice_debug=0;
      }
      else if (indice_debug>=100)
      { // deve esserci un errore
        fase_debug=3;
      }
      else
      {
        invia_byte_uart(char_debug);
        indice_debug++;
      }
    }
    else if (fase_debug==2)
    {
      unsigned char tempc;
      tempc=0;

      if (indice_debug==tempc++)       invia_byte_uart(' ');
      else if (indice_debug==tempc++)  invia_byte_uart('v');
      else if (indice_debug==tempc++)  invia_byte_uart('e');
      else if (indice_debug==tempc++)  invia_byte_uart('r');
      else if (indice_debug==tempc++)  invia_byte_uart(':');
      else if (indice_debug==tempc++)  invia_byte_uart(' ');
      else if (indice_debug==tempc++)  invia_byte_uart(hardware_version+'0');
      else if (indice_debug==tempc++)  invia_byte_uart('.');
      else if (indice_debug==tempc++)  invia_byte_uart(software_version+'0');
      else if (indice_debug==tempc++)  invia_byte_uart('.');
      else if (indice_debug==tempc++)  invia_byte_uart('r');
      else if (indice_debug==tempc++)  invia_byte_uart(software_revision/10+'0');
      else if (indice_debug==tempc++)  invia_byte_uart(software_revision%10+'0');
      else if (indice_debug==tempc++)
      {
        if (temporary_version)      invia_byte_uart('.');
        else
          fase_debug++;
      }
      else if (indice_debug==tempc++)  invia_byte_uart('t');
      else if (indice_debug==tempc++)  invia_byte_uart((temporary_version/10)+'0');
      else if (indice_debug==tempc++)  invia_byte_uart((temporary_version%10)+'0');
      else
        fase_debug++;
      indice_debug++;
    }
    else if (fase_debug==3)
    {
      invia_byte_uart(0xff);
      fase_debug=4;
      timer_pc_presente=timeout_uart;
    }
    else
    {
      if (timer_debug<10)
        timer_debug++;
      else
      {
        timer_debug=0;
        fase_debug=0;
        trasmetti_versione_232=0;
      }
    }
  }
//  else if (trasmetti_stringa_debug)
//  { // trasmetto una stringa dalla tabella
//    if (fase_debug==0)
//    {
//      if (timer_debug>100)
//      {
//        // faccio un check
//        if ((indice_stringa_debug>=numero_stringhe_debug)||(bak_indice_stringa_debug>=numero_stringhe_debug))
//        {
//          indice_stringa_debug=0;
//          bak_indice_stringa_debug=0;
//          trasmetti_stringa_debug=0;
//        }
//        else
//        { // inizio la trasmissione della stringa
//          invia_byte_uart(0xf4);
//          fase_debug++;
//          indice_debug=0;
//          timer_debug=0;
//        }
//      }
//      else timer_debug++;
//    }
//    else if (fase_debug==1)
//    { // invio la stringa fino al valore di finestringa o alla massima lunghezza
//      char_debug=stringa_debug[bak_indice_stringa_debug][indice_debug];
//      if (char_debug=='\0')
//      {
//        invia_byte_uart('\0');
//        fase_debug=2;
//      }
//      else if (indice_debug>=dimensione_stringa_debug)
//      { // deve esserci un errore
//        invia_byte_uart('\0');
//        fase_debug=2;
//      }
//      else
//      {
//        invia_byte_uart(char_debug);
//        indice_debug++;
//      }
//    }
//    else if (fase_debug==2)
//    {
//      invia_byte_uart(0xff);
//      fase_debug++;
//    }
//    else
//    {
//      if (timer_debug<100)
//        timer_debug++;
//      else
//      {
//        timer_debug=0;
//        fase_debug=0;
//        if (++bak_indice_stringa_debug>=numero_stringhe_debug)
//          bak_indice_stringa_debug=0;
////        if (indice_stringa_debug==bak_indice_stringa_debug)
//        trasmetti_stringa_debug=0;
//        // else trasmetti la stringa successiva
//        timer_pc_presente=timeout_uart;
//      }
//    }
//  }
  else if (trasmetti_nomi_tabelle)
  {
    if (fase_debug==0)
    {
      indice_tabella_var=0;
      if (timer_debug>100)
      {
        fase_debug++;
        timer_debug=0;
      }
      else timer_debug++;
    }
    else if (fase_debug==1)
    {
      if (indice_tabella_var<numero_tabelle_var)
      {
        fase_debug++;
        invia_byte_uart(0xf3);
      }
      else
      {
        trasmetti_nomi_tabelle=0;
        fase_debug=0;
      }
    }
    else if (fase_debug==2)
    {
      // Do not send index in the last tablet
      if (*tabella_var[indice_tabella_var].nome_tabella=='\0')
      	fase_debug=5;
      else
      {
      	invia_byte_uart(indice_tabella_var);
      	indice_debug=0;
      	fase_debug++;
      }
    }
    else if (fase_debug==3)
    {
      char_debug=*(tabella_var[indice_tabella_var].nome_tabella+indice_debug);

      if (char_debug=='\0')
      { // fine tabella variabili
        fase_debug++;
      }
      else if (indice_debug>=100)
      { // fine dello spazio
        fase_debug++;
      }
      else
      {
        invia_byte_uart(char_debug);
        indice_debug++;
      }
    }
    else if (fase_debug==4)
    {
    	if (tabella_var[indice_tabella_var].with_points)
    		invia_byte_uart(point_of_curve+1);
    	else
    		invia_byte_uart(tabella_var[indice_tabella_var].with_points);
    	fase_debug++;
    }
    else if (fase_debug==5)
    {
      invia_byte_uart(0xff);
      indice_tabella_var++;
      fase_debug=1;
    }
  }
  else if (trasmetti_nomi_delle_variabili_tabella)
  {
    if (fase_debug==0)
    { // carico la tabella

      if (tabella_var[indice_tabella_var].special==STEP_DEBUG_MIG_PULSE)
      {
//        debug_mig_pulse=1;
//      	debug_mig_std=0;
//      	machine_calibration=0;
      }
      else if (tabella_var[indice_tabella_var].special==STEP_DEBUG_MIG_STD)
      {
//      	debug_mig_pulse=0;
//        debug_mig_std=1;
//        machine_calibration=0;
      }
      else if (tabella_var[indice_tabella_var].special==STEP_DEBUG_CALIBRATION)
      {
//      	debug_mig_pulse=0;
//        debug_mig_std=0;
//        if (!machine_calibration)
//        	set_mma_current[mma_session]=0;
//        machine_calibration=1;
      }
      else
      {
//      	debug_mig_pulse=0;
//      	debug_mig_std=0;
//      	machine_calibration=0;
      }

      fase_debug++;
      timer_debug=0;
      indice_debug=0;
    }
    else if (fase_debug==1)
    { // trasmetto i nomi delle variabili con la seguente logica:
      // 0xf0,posizione,nome variabile,step,0xff

      // trasmetto il nome della variabile

      char_debug=*tabella_var[indice_tabella_var].var_tabella[indice_debug].nome_variabile;
      if (char_debug=='\0')
      { // fine tabella variabili
        fase_debug=200;
      }
      else if (indice_debug>=max_variabili_debug)
      { // fine dello spazio
        fase_debug=200;
      }
      else
      {
        fase_debug++;
        invia_byte_uart(0xf0);
      }
    }
    else if (fase_debug==2)
    {
      invia_byte_uart(indice_debug);
      fase_debug++;
    }
    else if (fase_debug<100)
    { // trasmetto il nome
      char_debug=*(tabella_var[indice_tabella_var].var_tabella[indice_debug].nome_variabile+fase_debug-3);
      if (char_debug=='\0')
      { // fine nome variabile
        fase_debug=100;
        // se invio 0 non viene gestito il +/-,
        // se trasmetto 1 viene gestito il +/-
        // se trasmetto 2 viene gestito il +/- ma si scrive ON/OFF
        if (tabella_var[indice_tabella_var].var_tabella[indice_debug].step==0)
          invia_byte_uart('0');
        else if (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_ON_OFF)
          invia_byte_uart('2');     // per i flag tipo on/off
        else if (tabella_var[indice_tabella_var].var_tabella[indice_debug].step==STEP_VOID)
          invia_byte_uart('0');     // titolo
        else if (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_STRING_RAM)
          invia_byte_uart('0');     // stringa
        else
          invia_byte_uart('1');
      }
      else
      {
        invia_byte_uart(char_debug);
        fase_debug++;
      }
    }
    else if (fase_debug==100)
    {
      fase_debug++;
      invia_byte_uart(0xff);
    }
    else if (fase_debug==STEP_VOID)
    {
      indice_debug++;
      fase_debug=1;
      timer_pc_presente=timeout_uart;
    }
    else if (fase_debug==200)
    {
      fase_debug++;
      invia_byte_uart(0xf0);
    }
    else if (fase_debug==201)
    {
      fase_debug++;
      invia_byte_uart(0xff);
    }
    else if (fase_debug==202)
    {
      trasmetti_nomi_delle_variabili_tabella=0;
      fase_debug=0;
      timer_debug=0;
      indice_debug=0;
    }
  }
  else if (trasmetti_valori_delle_variabili_tabella)
  {
    // invio le variabili secondo questa codifica:
    // 0xf1,posizione,dimensione variabile (1,2,4),variabile,0xff
    if (fase_debug==0)
    {
      indice_debug=0;
      fase_debug=1;
    }
    else if (fase_debug==1)
    { // cerco la variabile
      char_debug=*tabella_var[indice_tabella_var].var_tabella[indice_debug].nome_variabile;
      if (char_debug=='\0')
      { // fine tabella variabili
        invia_byte_uart(0xf1);
        fase_debug=202;
      }
      else if (indice_debug>=max_variabili_debug)
      { // fine dello spazio
        invia_byte_uart(0xf1);
        fase_debug=202;
      }
      else
      {
        fase_debug=2;
        invia_byte_uart(0xf1);
      }
    }
    else if (fase_debug==2)
    {
      invia_byte_uart(indice_debug);
      fase_debug=3;

      // leggo la variabile da trasferire
      var_debug=*tabella_var[indice_tabella_var].var_tabella[indice_debug].punta_variabile;
      if (tabella_var[indice_tabella_var].var_tabella[indice_debug].dimensione_variabile==1)
      {
        if ((tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN)||
            (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_1_DECIMAL)||
            (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_2_DECIMALS))
        {
      		if (var_debug>0x7f)
      		{
      		  var_debug=0x100-var_debug;
            segno_da_trasmettere='-';
      		}
      		else
            segno_da_trasmettere='+';
				}
      }
      else if (tabella_var[indice_tabella_var].var_tabella[indice_debug].dimensione_variabile==2)
      {
        var_debug=var_debug+(*(tabella_var[indice_tabella_var].var_tabella[indice_debug].punta_variabile+1))*256;
        if ((tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN)||
            (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_1_DECIMAL)||
            (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_2_DECIMALS))
      	{
      		if (var_debug>0x7fff)
      		{
        		var_debug=0x10000-var_debug;
            segno_da_trasmettere='-';
      		}
      		else
            segno_da_trasmettere='+';
      	}
      }
      else if (tabella_var[indice_tabella_var].var_tabella[indice_debug].dimensione_variabile==4)
      {
        var_debug=var_debug+*(tabella_var[indice_tabella_var].var_tabella[indice_debug].punta_variabile+1)*256;
        var_debug=var_debug+*(tabella_var[indice_tabella_var].var_tabella[indice_debug].punta_variabile+2)*(256*256);
        var_debug=var_debug+*(tabella_var[indice_tabella_var].var_tabella[indice_debug].punta_variabile+3)*(256*256*256);
        if ((tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN)||
            (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_1_DECIMAL)||
            (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_2_DECIMALS))
      	{
      		if (var_debug>0x7fffffff)
      		{
  					var_debug=0x100000000-var_debug;
            segno_da_trasmettere='-';
      		}
      		else
            segno_da_trasmettere='+';
      	}
      }
      else
      { // do per scontato che sia una stringa
      }

      // trasformo il numero da trasmettere in una stringa
      if (tabella_var[indice_tabella_var].var_tabella[indice_debug].step==STEP_VOID)
      {
        carat_debug[punta_carat_debug++]=' ';
      }
      else if (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_ON_OFF)
      { // le stringhe le carico rovesce
        if (var_debug==0)
        {
          carat_debug[punta_carat_debug++]='F';
          carat_debug[punta_carat_debug++]='F';
          carat_debug[punta_carat_debug++]='O';
        }
        else
        {
          carat_debug[punta_carat_debug++]='N';
          carat_debug[punta_carat_debug++]='O';
        }
      }
      else if (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_STRING_RAM)
      { // invio la stringa
        unsigned char pt;

        pt=tabella_var[indice_tabella_var].var_tabella[indice_debug].dimensione_variabile;
        if (pt>30) pt=30;
        while (pt)
        {
          pt--;
          carat_debug[punta_carat_debug++]=*(tabella_var[indice_tabella_var].var_tabella[indice_debug].punta_variabile+pt);
        }
      }
      else if (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_STRING_CONST)
      { // invio la stringa, la variabile e' un puntatore, devo cercare la fine stringa e poi rovesciarla
        unsigned char pt;
        unsigned char *puntavar;
        unsigned char buf[16];

        pt=0;
        puntavar=(unsigned char *)var_debug;

        while (pt<16)
        {
          buf[punta_carat_debug]=*puntavar++;
          if (buf[punta_carat_debug]=='\0')
            pt=16;
          else
            pt++;
          punta_carat_debug++;
        }
        // rovescio la stringa
        pt=punta_carat_debug-1;
        punta_carat_debug=0;
        while (pt)
        {
          pt--;
          carat_debug[punta_carat_debug++]=buf[pt];
        }
      }
      else
      { // numero
        punta_carat_debug=0;

        while (var_debug)
        {
          carat_debug[punta_carat_debug++]=var_debug%10+'0';
          var_debug=var_debug/10;
          if ((tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_1_DECIMAL)||
              (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_1_DECIMAL))
          { // variabile con 1 decimale
            if (punta_carat_debug==1)
              carat_debug[punta_carat_debug++]=',';
          }
          else if ((tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_2_DECIMALS)||
          				 (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_2_DECIMALS))
          { // variabile con 2 decimali
            if (punta_carat_debug==2)
              carat_debug[punta_carat_debug++]=',';
          }
        }

        if ((tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_1_DECIMAL)||
            (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_1_DECIMAL))
        { // variabile con 1 decimale
          if (!punta_carat_debug)
          {
            carat_debug[punta_carat_debug++]='0';
            carat_debug[punta_carat_debug++]=',';
            carat_debug[punta_carat_debug++]='0';
          }
          else if (punta_carat_debug==2)
            carat_debug[punta_carat_debug++]='0';
        }
        else if ((tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_2_DECIMALS)||
        				 (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_2_DECIMALS))
        { // variabile con 2 decimali
          if (!punta_carat_debug)
          {
            carat_debug[punta_carat_debug++]='0';
            carat_debug[punta_carat_debug++]='0';
            carat_debug[punta_carat_debug++]=',';
            carat_debug[punta_carat_debug++]='0';
          }
          else if (punta_carat_debug==1)
          {
            carat_debug[punta_carat_debug++]='0';
            carat_debug[punta_carat_debug++]=',';
            carat_debug[punta_carat_debug++]='0';
          }
          else if (punta_carat_debug==2)
            carat_debug[punta_carat_debug++]='0';
        }
        else if (!punta_carat_debug)
        {
          carat_debug[punta_carat_debug++]='0';
        }

        if ((tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN)||
            (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_1_DECIMAL)||
            (tabella_var[indice_tabella_var].var_tabella[indice_debug].type_var==TYPE_VAR_WITH_SIGN_AND_2_DECIMALS))
          carat_debug[punta_carat_debug++]=segno_da_trasmettere;

      	if (!punta_carat_debug)
          carat_debug[punta_carat_debug++]='0';
      }
    }
    else if (fase_debug<100)
    { // trasmetto la variabile a caratteri come la visualizzerei
      if (punta_carat_debug)
      { // trasmetto il carattere
        punta_carat_debug--;
//        if (carat_debug[punta_carat_debug]<=9)
//          invia_byte_uart(carat_debug[punta_carat_debug]+'0');
        if (carat_debug[punta_carat_debug]=='\0')
        	punta_carat_debug=0;
        else
          invia_byte_uart(carat_debug[punta_carat_debug]);
      }
      else
      { // trasmetto il carattere di fine stringa
        fase_debug=1;
        indice_debug++;
        timer_pc_presente=timeout_uart;
        invia_byte_uart(0xff);
      }
    }
    // 0xf1,posizione,dimensione variabile (1,2,4),variabile,0xff
    else if (fase_debug==200)
    {
      fase_debug++;
      invia_byte_uart(0xf1);
    }
    else if (fase_debug==201)
    {
      fase_debug++;
//      if (in_weld)
//      	invia_byte_uart(100);
//      else if (inverter_on)
//      	invia_byte_uart(100);
//      else if (in_cycle)
//      	invia_byte_uart(101);
//      else
      	invia_byte_uart(102);
    }
    else if (fase_debug==202)
    {
      fase_debug++;
      invia_byte_uart(0xff);
    }
    else if (fase_debug==203)
    {
      fase_debug=0;
      timer_debug=0;
      trasmetti_valori_delle_variabili_tabella=0;
//      if (indice_stringa_debug!=bak_indice_stringa_debug)
//      	trasmetti_stringa_debug=1;
    }
  }
  else if (cambia_tabella)
  {
    unsigned char index;
    index=cambia_tabella-'0';
    cambia_tabella=0;
    if (index<numero_tabelle_var)
    {
      indice_tabella_var=index;
      trasmetti_nomi_delle_variabili_tabella=1;
      timer_pc_presente=timeout_uart;
      fase_debug=0;
    }
  }
  else
  {
  }
}






//*******************************************************************************
void invia_byte_uart(unsigned char dato_uart)
{
	UART_DEBUG->TDR=dato_uart;
}
//*******************************************************************************
//*******************************************************************************



