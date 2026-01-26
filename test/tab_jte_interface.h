
// tab_jte_interface.h

unsigned char var_vuota;
extern unsigned char schermata, fase_schermata, colore_sfondo, colore_attivo;
extern unsigned char fase_var;

/*
note d'uso:

la prima variabile e' solo un titolo e appare nel PC in grassetto,

step_debug e' facoltativo, se non c'e' e' come se fosse a 0
step_debug puo' essere un numero qualsiasi (tranne alcune eccezioni),

se il comando arriva 2 volte entro 1 secondo lo step viene moltiplicato per 10

se step_debug e' 101 la variabile spedita e' uno spazio vuoto e non viene visualizzato niente
se step_debug e' 99 viene spedito ON/OFF come se fosse un flag
se step_debug e' 102 viene inviata una stringa

*/



extern unsigned char font;
extern unsigned short bak_data_oled[];

extern unsigned char st_phase;

var_da_debuggare tabella_var_da_debuggare_debug[]={
{"DEBUG",(char*)&var_vuota,sizeof(var_vuota),101},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"phase_st_protocol",(char*)&phase_st_protocol,sizeof(phase_st_protocol)},
{"timer_st_protocol",(char*)&timer_st_protocol,sizeof(timer_st_protocol)},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"power_on_number",(char*)&power_on_number,sizeof(power_on_number)},
{"new_power_on_number",(char*)&new_power_on_number,sizeof(new_power_on_number)},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"oled_phase",(char*)&oled_phase,sizeof(oled_phase)},
{"timer_10ms_oled",(char*)&timer_10ms_oled,sizeof(timer_10ms_oled)},


//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"st_phase",(char*)&st_phase,sizeof(st_phase)},
//{"st_timer",(char*)&st_timer,sizeof(st_timer)},
//{"st_in_value_average",(char*)&st_in_value_average,sizeof(st_in_value_average)},
//{"st_in_value_min",(char*)&st_in_value_min,sizeof(st_in_value_min)},
//{"st_in_value_threshold_l",(char*)&st_in_value_threshold_l,sizeof(st_in_value_threshold_l)},
//{"st_in_value_threshold_h",(char*)&st_in_value_threshold_h,sizeof(st_in_value_threshold_h)},


//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"set_mode",(char*)&set_mode,sizeof(set_mode)},

//{"set_cycle",(char*)&set_cycle,sizeof(set_cycle)},


//{"max_bt_1ms(us)",(char*)&max_bt_1ms,sizeof(max_bt_1ms)},
//{"average_bt_1ms(us)",(char*)&average_bt_1ms,sizeof(average_bt_1ms)},



//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"counter_sw1",(char*)&counter_sw1,sizeof(counter_sw1)},
//{"counter_sw2",(char*)&counter_sw2,sizeof(counter_sw1)},
////{"counter_sw12",(char*)&counter_sw12,sizeof(counter_sw12)},
//{"counter_sw3",(char*)&counter_sw3,sizeof(counter_sw1)},
//{"counter_swup",(char*)&counter_swUp,sizeof(counter_swUp)},
//{"counter_pt_mig",(char*)&counter_pt_mig,sizeof(counter_pt_mig)},
//{"counter_pt_tig",(char*)&counter_pt_tig,sizeof(counter_pt_tig)},



{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"dip_status",(char*)&dip_status,sizeof(dip_status)},
{"dip_type",(char*)&dip_type,sizeof(dip_type)},

{"identity_card_type1_value",(char*)&identity_card_type1_value,sizeof(identity_card_type1_value)},
{"identity_card_type1",(char*)&identity_card_type1,sizeof(identity_card_type1)},
{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"identity_card_type2_value",(char*)&identity_card_type2_value,sizeof(identity_card_type2_value)},
{"identity_card_type2",(char*)&identity_card_type2,sizeof(identity_card_type2)},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"set_type",(char*)&set_type,sizeof(set_type),1},
//{"set_cycle",(char*)&set_cycle,sizeof(set_cycle),1},
//{"tig_set_hf",(char*)&tig_set_hf,sizeof(tig_set_hf),1},



//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"my_configuration",(char*)&my_configuration,sizeof(my_configuration),1},
//{"week_start",(char*)&week_start,sizeof(week_start)},
//{"year_start",(char*)&year_start,sizeof(year_start)},
//{"power_on_number",(char*)&power_on_number,sizeof(power_on_number)},
//{"life_cycle_1 (start cycle)",(char*)&life_cycle_1,sizeof(life_cycle_1)},
//{"life_cycle_2 (min.use)",(char*)&life_cycle_2,sizeof(life_cycle_2)},
//{"life_cycle_3 (min.cons.)",(char*)&life_cycle_3,sizeof(life_cycle_3)},
//{"alarm_flash",(char*)&alarm_flash,sizeof(alarm_flash)},
//
//
//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"new_week_start",(char*)&new_week_start,sizeof(new_week_start),1},
//{"new_year_start",(char*)&new_year_start,sizeof(new_year_start),1},
//{"new_power_on_number",(char*)&new_power_on_number,sizeof(new_power_on_number),1},
//{"new_life_cycle_1 (start cycle)",(char*)&new_life_cycle_1,sizeof(new_life_cycle_1),1},
//{"new_life_cycle_2 (min.use)",(char*)&new_life_cycle_2,sizeof(new_life_cycle_2),1},
//{"new_life_cycle_3 (min.cons.)",(char*)&new_life_cycle_3,sizeof(new_life_cycle_3),1},





//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"cpu_uid_long[0]",(char*)&cpu_uid_long[0],sizeof(cpu_uid_long[0])},
//{"cpu_uid_long[1]",(char*)&cpu_uid_long[1],sizeof(cpu_uid_long[1])},
//{"cpu_uid_long[2]",(char*)&cpu_uid_long[2],sizeof(cpu_uid_long[2])},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},


{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"st_packed_for_second",(char*)&st_packed_for_second,sizeof(st_packed_for_second)},


{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"temperature",(char*)&temperature,sizeof(temperature)},


{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"menu_display",(char*)&menu_display,sizeof(menu_display),1},

//{"set_lumen",(char*)&set_lumen,sizeof(set_lumen)},
//{"timer_lumen",(char*)&timer_lumen,sizeof(timer_lumen)},
//
//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"bar_value",(char*)&bar_value,sizeof(bar_value)},
//{"dbar_value",(char*)&dbar_value,sizeof(dbar_value)},
//
//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"weld_current",(char*)&weld_current,sizeof(weld_current)},
//{"weld_voltage",(char*)&weld_voltage,sizeof(weld_voltage)},

//{"font",(char*)&font,sizeof(font),1},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"sw1",(char*)&sw1,sizeof(sw1),1},
//{"sw2",(char*)&sw2,sizeof(sw1),1},
//{"sw3",(char*)&sw3,sizeof(sw1),1},

//{"counter_pt",(char*)&counter_pt,sizeof(counter_pt),1},


//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"tig_set_type",(char*)&tig_set_type,sizeof(tig_set_type),1},

{"set_current",(char*)&set_current,sizeof(set_current),1},




//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"st_timer_between_packet",(char*)&st_timer_between_packet,sizeof(st_timer_between_packet),1},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"bak_data_oled",(char*)&bak_data_oled,sizeof(bak_data_oled),1},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"ms_to_refresh_oled",(char*)&ms_to_refresh_oled,sizeof(ms_to_refresh_oled)},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},




//{"st_phase",(char*)&st_phase_old,sizeof(st_phase_old)},
//{"st_timer",(char*)&st_timer,sizeof(st_timer)},
//{"st_in_value_average",(char*)&st_in_value_average,sizeof(st_in_value_average)},
//{"st_in_value_threshold",(char*)&st_in_value_threshold,sizeof(st_in_value_threshold)},
//
//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"pot_value",(char*)&pot_value,sizeof(pot_value)},
//{"new_pot_value",(char*)&new_pot_value,sizeof(new_pot_value)},
//{"temperature",(char*)&temperature,sizeof(temperature)},
//{"cpu_temperature",(char*)&cpu_temperature,sizeof(cpu_temperature)},
//{"my_vrefint",(char*)&my_vrefint,sizeof(my_vrefint)},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"st_status",(char*)&st_status,sizeof(st_status)},
//{"st_tx_data.st_data.command_byte",(char*)&st_tx_data.st_data.command_byte,sizeof(st_tx_data.st_data.command_byte),1},
//{"st_tx_data.st_data.data_byte",(char*)&st_tx_data.st_data.data_byte,sizeof(st_tx_data.st_data.data_byte)},



{"test_menu_debug",(char*)&test_menu_debug,sizeof(test_menu_debug),1},
{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"st_rx_data",(char*)&st_rx_data,sizeof(st_rx_data)},
{"st_rx_command_byte",(char*)&st_rx_command_byte,sizeof(st_rx_command_byte),1},
{"st_rx_data_byte",(char*)&st_rx_data_byte,sizeof(st_rx_data_byte)},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"sw1",(char*)&sw1,sizeof(sw1)},
{"sw2",(char*)&sw2,sizeof(sw1)},
{"sw3",(char*)&sw3,sizeof(sw1)},
//{"sw4",(char*)&sw4,sizeof(sw1)},
{"counter_sw1",(char*)&counter_sw1,sizeof(counter_sw1)},
{"counter_sw2",(char*)&counter_sw2,sizeof(counter_sw1)},
{"counter_sw3",(char*)&counter_sw3,sizeof(counter_sw1)},

{"sw12",(char*)&sw12,sizeof(sw12)},
{"counter_sw12",(char*)&counter_sw12,sizeof(counter_sw12)},
{"sw23",(char*)&sw23,sizeof(sw23)},
{"counter_sw23",(char*)&counter_sw23,sizeof(counter_sw23)},
//{"seconds_lcd",(char*)&seconds_lcd,sizeof(seconds_lcd)},

//{"timer_1ms_oled",(char*)&timer_1ms_oled,sizeof(timer_1ms_oled)},

//{"phase_pt_clk",(char*)&phase_pt_clk,sizeof(phase_pt_clk),1},


{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"seconds",(char*)&seconds,sizeof(seconds)},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"debug_flash",(char*)&debug_flash,sizeof(debug_flash),1},
//{"indirizzo_ultima_locazione_letta",(char*)&indirizzo_ultima_locazione_letta,sizeof(indirizzo_ultima_locazione_letta),1},
//{"indirizzo_ultima_locazione_scritta",(char*)&indirizzo_ultima_locazione_scritta,sizeof(indirizzo_ultima_locazione_scritta),1},
//{"pagine_cancellate",(char*)&pagine_cancellate,sizeof(pagine_cancellate),1},
//{"ultima_pagina_cancellata",(char*)&ultima_pagina_cancellata,sizeof(ultima_pagina_cancellata),1},




{" ",(char*)&var_vuota,sizeof(var_vuota),101},
{"debug1",(char*)&debug1,sizeof(debug1),1},
{"debug2",(char*)&debug2,sizeof(debug1),1},
{"debug3",(char*)&debug3,sizeof(debug1),1},
{"debug4",(char*)&debug4,sizeof(debug1),1},
{"debug5",(char*)&debug5,sizeof(debug1),1},
{"debug6",(char*)&debug6,sizeof(debug1),1},
{"debug7",(char*)&debug7,sizeof(debug1),1},
{"debug8",(char*)&debug8,sizeof(debug1),1},
{"debug9",(char*)&debug9,sizeof(debug1),1},
{"debug10",(char*)&debug10,sizeof(debug1),1},

{""},				// questa riga deve restare sempre!!!
};


var_da_debuggare tabella_var_da_debuggare_config[]={
{"CONFIG DATA",(char*)&var_vuota,sizeof(var_vuota),101},

//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"dip_type",(char*)&dip_type,sizeof(dip_type)},
//{"identity_card_type",(char*)&identity_card_type,sizeof(identity_card_type)},
//{"identity_card_type2",(char*)&identity_card_type2,sizeof(identity_card_type2)},


{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"my_configuration",(char*)&my_configuration,sizeof(my_configuration),1},
{"week_start",(char*)&week_start,sizeof(week_start)},
{"year_start",(char*)&year_start,sizeof(year_start)},
{"power_on_number",(char*)&power_on_number,sizeof(power_on_number)},
{"life_cycle_1 (start cycle)",(char*)&life_cycle_1,sizeof(life_cycle_1)},
{"life_cycle_2 (min.use)",(char*)&life_cycle_2,sizeof(life_cycle_2)},
{"life_cycle_3 (min.cons.)",(char*)&life_cycle_3,sizeof(life_cycle_3)},
{"alarm_flash",(char*)&alarm_flash,sizeof(alarm_flash)},


{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"new_week_start",(char*)&new_week_start,sizeof(new_week_start),1},
{"new_year_start",(char*)&new_year_start,sizeof(new_year_start),1},
{"new_power_on_number",(char*)&new_power_on_number,sizeof(new_power_on_number),1},
{"new_life_cycle_1 (start cycle)",(char*)&new_life_cycle_1,sizeof(new_life_cycle_1),1},
{"new_life_cycle_2 (min.use)",(char*)&new_life_cycle_2,sizeof(new_life_cycle_2),1},
{"new_life_cycle_3 (min.cons.)",(char*)&new_life_cycle_3,sizeof(new_life_cycle_3),1},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
//{"debug_flash",(char*)&debug_flash,sizeof(debug_flash),1},
{"indirizzo_ultima_locazione_letta",(char*)&indirizzo_ultima_locazione_letta,sizeof(indirizzo_ultima_locazione_letta),1},
{"indirizzo_ultima_locazione_scritta",(char*)&indirizzo_ultima_locazione_scritta,sizeof(indirizzo_ultima_locazione_scritta),1},
{"pagine_cancellate",(char*)&pagine_cancellate,sizeof(pagine_cancellate),1},
{"ultima_pagina_cancellata",(char*)&ultima_pagina_cancellata,sizeof(ultima_pagina_cancellata),1},

//{" ",(char*)&var_vuota,sizeof(var_vuota),101},
//{"debug1",(char*)&debug1,sizeof(debug1),1},
//{"debug2",(char*)&debug2,sizeof(debug1),1},
//{"debug3",(char*)&debug3,sizeof(debug1),1},
//{"debug4",(char*)&debug4,sizeof(debug1),1},
//{"debug5",(char*)&debug5,sizeof(debug1),1},
//{"debug6",(char*)&debug6,sizeof(debug1),1},
//{"debug7",(char*)&debug7,sizeof(debug1),1},
//{"debug8",(char*)&debug8,sizeof(debug1),1},
//{"debug9",(char*)&debug9,sizeof(debug1),1},
//{"debug10",(char*)&debug10,sizeof(debug1),1},

{""},       // questa riga deve restare sempre!!!
};





var_da_debuggare tabella_var_da_debuggare_adc1[]={
{"ADC",(char*)&var_vuota,sizeof(var_vuota),101},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"error_adc1",(char*)&error_adc1,sizeof(error_adc1),1},
{"error_dma_adc1",(char*)&error_dma_adc1,sizeof(error_dma_adc1),1},
{"error_int_dma1_ch1_adc1",(char*)&error_int_dma1_ch1_adc1,sizeof(error_int_dma1_ch1_adc1),1},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"instant_pot",(char*)&instant_pot,sizeof(instant_pot)},
{"pot_value",(char*)&pot_value,sizeof(pot_value)},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"instant_ntc1",(char*)&instant_ntc1,sizeof(instant_ntc1)},
{"temperature",(char*)&temperature,sizeof(temperature)},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"instant_identity_card_dip1_pt",(char*)&instant_identity_card_dip1_pt,sizeof(instant_identity_card_dip1_pt)},
{"value_pt",(char*)&value_pt,sizeof(value_pt)},
{"pt_sw",(char*)&pt_sw,sizeof(pt_sw)},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"instant_identity_card_dip2",(char*)&instant_identity_card_dip2,sizeof(instant_identity_card_dip2)},
//{"temperature",(char*)&temperature,sizeof(temperature)},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"instant_data_in",(char*)&instant_data_in,sizeof(instant_data_in)},



{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"instant_cpu_temperature",(char*)&instant_cpu_temperature,sizeof(instant_cpu_temperature)},
{"cpu_temperature_30",(char*)&cpu_temperature_30,sizeof(cpu_temperature_30)},
{"cpu_temperature_130",(char*)&cpu_temperature_130,sizeof(cpu_temperature_130)},
{"cpu_temperature",(char*)&cpu_temperature,sizeof(cpu_temperature)},

{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},
{"instant_vrefint",(char*)&instant_vrefint,sizeof(instant_vrefint)},
{"my_vrefint",(char*)&my_vrefint,sizeof(my_vrefint)},
{"my_vrefint_true",(char*)&my_vrefint_true,sizeof(my_vrefint_true)},


{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},


//{" ",(char*)&titolo,sizeof(titolo),STEP_VOID},




//{" ",(char*)&var_vuota,sizeof(var_vuota),101},
//{"debug1",(char*)&debug1,sizeof(debug1),1},
//{"debug2",(char*)&debug2,sizeof(debug1),1},
//{"debug3",(char*)&debug3,sizeof(debug1),1},
//{"debug4",(char*)&debug4,sizeof(debug1),1},
//{"debug5",(char*)&debug5,sizeof(debug1),1},
//{"debug6",(char*)&debug6,sizeof(debug1),1},
//{"debug7",(char*)&debug7,sizeof(debug1),1},
//{"debug8",(char*)&debug8,sizeof(debug1),1},
//{"debug9",(char*)&debug9,sizeof(debug1),1},
//{"debug10",(char*)&debug10,sizeof(debug1),1},

{""},       // questa riga deve restare sempre!!!
};







// posso gestirne al massimo 9, non spostare l'ordine delle tabelle, metti a 1 se vuoi gestire i punti
const tipo_tabella_var  tabella_var[]={

{"DEBUG",&tabella_var_da_debuggare_debug[0],0},
{"CONFIG DATA",&tabella_var_da_debuggare_config[0],0},
{"ADC1",&tabella_var_da_debuggare_adc1[0],0},
{""},				// questa riga deve restare sempre!!!
};





