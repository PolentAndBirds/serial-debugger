VERSION 5.00
Object = "{648A5603-2C6E-101B-82B6-000000000014}#1.1#0"; "MSComm32.Ocx"
Object = "{5E9E78A0-531B-11CF-91F6-C2863C385E30}#1.0#0"; "MSFlxGrd.ocx"
Object = "{F9043C88-F6F2-101A-A3C9-08002B2F49FB}#1.2#0"; "ComDlg32.OCX"
Object = "{3B7C8863-D78F-101B-B9B5-04021C009402}#1.2#0"; "richtx32.Ocx"
Begin VB.Form tercm 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "TER CONFIGURATION MANAGER"
   ClientHeight    =   9588
   ClientLeft      =   5664
   ClientTop       =   780
   ClientWidth     =   17064
   BeginProperty Font 
      Name            =   "Courier New"
      Size            =   12
      Charset         =   0
      Weight          =   700
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   Icon            =   "tcm.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   9588
   ScaleWidth      =   17064
   Begin VB.CommandButton tasto_debug 
      Caption         =   "->"
      Enabled         =   0   'False
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   7.8
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   372
      Left            =   11040
      TabIndex        =   44
      Top             =   840
      Width           =   372
   End
   Begin VB.CommandButton tasto_abort 
      Caption         =   "ABORT"
      Enabled         =   0   'False
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   16.2
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   972
      Left            =   8760
      TabIndex        =   43
      Top             =   8520
      Visible         =   0   'False
      Width           =   2652
   End
   Begin VB.CommandButton comando_clear_seriale 
      Caption         =   "CLEAR"
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   13.8
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   492
      Left            =   11640
      TabIndex        =   42
      Top             =   120
      Width           =   2052
   End
   Begin VB.TextBox text_debug3 
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   13.8
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   492
      Left            =   15960
      TabIndex        =   41
      Text            =   "Text1"
      Top             =   120
      Width           =   972
   End
   Begin VB.TextBox text_debug2 
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   13.8
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   492
      Left            =   14880
      TabIndex        =   40
      Text            =   "Text1"
      Top             =   120
      Width           =   972
   End
   Begin VB.TextBox text_debug1 
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   13.8
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   492
      Left            =   13800
      TabIndex        =   39
      Text            =   "Text1"
      Top             =   120
      Width           =   972
   End
   Begin VB.TextBox totale_righe 
      Height          =   396
      Left            =   13800
      TabIndex        =   38
      Top             =   9000
      Width           =   2892
   End
   Begin VB.TextBox totale_byte 
      Height          =   396
      Left            =   13800
      TabIndex        =   37
      Top             =   8400
      Width           =   2892
   End
   Begin RichTextLib.RichTextBox text_report 
      Height          =   6132
      Left            =   1440
      TabIndex        =   34
      Top             =   1440
      Width           =   6372
      _ExtentX        =   11240
      _ExtentY        =   10816
      _Version        =   393217
      BackColor       =   16777215
      TextRTF         =   $"tcm.frx":014A
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Courier New"
         Size            =   12
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
   End
   Begin MSComDlg.CommonDialog CommonDialog1 
      Left            =   13680
      Top             =   6600
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
   End
   Begin VB.Frame frame_update 
      Caption         =   "UPDATE FIRMWARE"
      Height          =   2532
      Left            =   8760
      TabIndex        =   26
      Top             =   2760
      Width           =   2652
      Begin VB.CommandButton tasto_recall_report 
         Caption         =   "RECALL REPORT"
         Enabled         =   0   'False
         BeginProperty Font 
            Name            =   "Courier New"
            Size            =   12
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   372
         Left            =   120
         TabIndex        =   33
         Top             =   2040
         Width           =   2412
      End
      Begin VB.ComboBox combo_device 
         Height          =   372
         ItemData        =   "tcm.frx":01D3
         Left            =   120
         List            =   "tcm.frx":01D5
         TabIndex        =   32
         Text            =   "sel.device"
         Top             =   840
         Width           =   2412
      End
      Begin VB.CommandButton tasto_update 
         Caption         =   "UPDATE"
         BeginProperty Font 
            Name            =   "Courier New"
            Size            =   16.2
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   612
         Left            =   120
         TabIndex        =   27
         Top             =   1320
         Width           =   2412
      End
      Begin VB.Label label_file_hex 
         Alignment       =   2  'Center
         BorderStyle     =   1  'Fixed Single
         Caption         =   "SELECT FILE"
         Height          =   372
         Left            =   120
         TabIndex        =   29
         Top             =   360
         Width           =   2412
      End
   End
   Begin VB.TextBox text_macchina 
      BackColor       =   &H8000000F&
      BorderStyle     =   0  'None
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   16.2
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   372
      Left            =   240
      Locked          =   -1  'True
      TabIndex        =   25
      Text            =   "SELECT COM PORT & CLICK START"
      Top             =   120
      Width           =   8016
   End
   Begin VB.CommandButton tasto_extra 
      Caption         =   "T"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.2
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   372
      Left            =   13080
      TabIndex        =   24
      Top             =   6720
      Visible         =   0   'False
      Width           =   372
   End
   Begin VB.Timer Timer1 
      Interval        =   50
      Left            =   11640
      Top             =   6600
   End
   Begin VB.Frame frame_tabelle 
      Caption         =   "DATA TYPE"
      Height          =   1692
      Left            =   8760
      TabIndex        =   23
      Top             =   6600
      Visible         =   0   'False
      Width           =   2652
      Begin VB.ComboBox combo_tabelle 
         BackColor       =   &H8000000D&
         BeginProperty Font 
            Name            =   "Courier New"
            Size            =   16.2
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   456
         ItemData        =   "tcm.frx":01D7
         Left            =   120
         List            =   "tcm.frx":01D9
         TabIndex        =   30
         Text            =   "tabelle"
         Top             =   360
         Visible         =   0   'False
         Width           =   2412
      End
      Begin VB.CommandButton tasto_selezione_tabella 
         Caption         =   "SELECT"
         BeginProperty Font 
            Name            =   "Courier New"
            Size            =   16.2
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   612
         Left            =   120
         TabIndex        =   28
         Top             =   960
         Width           =   2412
      End
   End
   Begin VB.TextBox seriale 
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   10.2
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   5652
      Left            =   11640
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   22
      Top             =   720
      Width           =   5292
   End
   Begin VB.Frame frame_com 
      Caption         =   "PC COMM PORT"
      Height          =   732
      Left            =   8760
      TabIndex        =   11
      Top             =   600
      Width           =   2052
      Begin VB.OptionButton Option2 
         Caption         =   "4"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   3
         Left            =   1440
         TabIndex        =   15
         Top             =   360
         Width           =   372
      End
      Begin VB.OptionButton Option2 
         Caption         =   "3"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   2
         Left            =   1080
         TabIndex        =   14
         Top             =   360
         Width           =   372
      End
      Begin VB.OptionButton Option2 
         Caption         =   "2"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   1
         Left            =   600
         TabIndex        =   13
         Top             =   360
         Width           =   372
      End
      Begin VB.OptionButton Option2 
         Caption         =   "1"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   0
         Left            =   120
         TabIndex        =   12
         Top             =   360
         Width           =   375
      End
   End
   Begin VB.Frame frame_punti 
      Caption         =   "Load Point"
      Height          =   1092
      Left            =   8760
      TabIndex        =   5
      Top             =   8400
      Visible         =   0   'False
      Width           =   2652
      Begin VB.OptionButton Option1 
         Caption         =   "10"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   9
         Left            =   2040
         TabIndex        =   20
         Top             =   720
         Width           =   440
      End
      Begin VB.OptionButton Option1 
         Caption         =   "9"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   8
         Left            =   1560
         TabIndex        =   19
         Top             =   720
         Width           =   440
      End
      Begin VB.OptionButton Option1 
         Caption         =   "8"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   7
         Left            =   1080
         TabIndex        =   18
         Top             =   720
         Width           =   440
      End
      Begin VB.OptionButton Option1 
         Caption         =   "7"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   6
         Left            =   600
         TabIndex        =   17
         Top             =   720
         Width           =   440
      End
      Begin VB.OptionButton Option1 
         Caption         =   "6"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   5
         Left            =   120
         TabIndex        =   16
         Top             =   720
         Width           =   440
      End
      Begin VB.OptionButton Option1 
         Caption         =   "5"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   4
         Left            =   2040
         TabIndex        =   10
         Top             =   360
         Width           =   440
      End
      Begin VB.OptionButton Option1 
         Caption         =   "4"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   3
         Left            =   1560
         TabIndex        =   9
         Top             =   360
         Width           =   440
      End
      Begin VB.OptionButton Option1 
         Caption         =   "3"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   2
         Left            =   1080
         TabIndex        =   8
         Top             =   360
         Width           =   440
      End
      Begin VB.OptionButton Option1 
         Caption         =   "2"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   1
         Left            =   600
         TabIndex        =   7
         Top             =   360
         Width           =   440
      End
      Begin VB.OptionButton Option1 
         Caption         =   "1"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   7.8
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Index           =   0
         Left            =   120
         TabIndex        =   6
         Top             =   360
         Width           =   440
      End
   End
   Begin VB.Frame frame_comandi 
      Caption         =   "RESET COMMANDS"
      Height          =   1092
      Left            =   8760
      TabIndex        =   3
      Top             =   5400
      Width           =   2652
      Begin VB.CommandButton comando_reset 
         Caption         =   "SOFT"
         BeginProperty Font 
            Name            =   "Courier New"
            Size            =   16.2
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   612
         Index           =   1
         Left            =   1440
         TabIndex        =   21
         Top             =   360
         Width           =   1092
      End
      Begin VB.CommandButton comando_reset 
         Caption         =   "HARD"
         BeginProperty Font 
            Name            =   "Courier New"
            Size            =   16.2
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   612
         Index           =   0
         Left            =   120
         TabIndex        =   4
         Top             =   360
         Width           =   1092
      End
   End
   Begin MSFlexGridLib.MSFlexGrid win 
      Height          =   8796
      Left            =   120
      TabIndex        =   2
      Top             =   720
      Width           =   8496
      _ExtentX        =   14986
      _ExtentY        =   15515
      _Version        =   393216
      Rows            =   50
      Cols            =   5
      FixedRows       =   0
      FixedCols       =   0
      ScrollBars      =   2
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Courier New"
         Size            =   13.8
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
   End
   Begin VB.CommandButton tasto_exit 
      Caption         =   "EXIT"
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   16.2
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   972
      Left            =   10200
      TabIndex        =   1
      Top             =   1560
      Width           =   1212
   End
   Begin VB.CommandButton tasto_uart 
      Caption         =   "START"
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   16.2
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   972
      Left            =   8760
      TabIndex        =   0
      Top             =   1560
      Width           =   1212
   End
   Begin MSCommLib.MSComm uart 
      Left            =   12240
      Top             =   6600
      _ExtentX        =   995
      _ExtentY        =   995
      _Version        =   393216
      DTREnable       =   -1  'True
      RThreshold      =   1
      BaudRate        =   19200
   End
   Begin VB.Label Label1 
      Caption         =   "Totale righe"
      Height          =   252
      Index           =   1
      Left            =   11760
      TabIndex        =   36
      Top             =   9120
      Width           =   1932
   End
   Begin VB.Label Label1 
      Caption         =   "Totale bytes"
      Height          =   252
      Index           =   0
      Left            =   11760
      TabIndex        =   35
      Top             =   8520
      Width           =   1932
   End
   Begin VB.Label label_timeout 
      BorderStyle     =   1  'Fixed Single
      Caption         =   "timeout"
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   13.8
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   372
      Left            =   8760
      TabIndex        =   31
      Top             =   120
      Visible         =   0   'False
      Width           =   2652
   End
   Begin VB.Shape puntatore 
      BorderColor     =   &H000000FF&
      BorderStyle     =   6  'Inside Solid
      FillColor       =   &H00FF0000&
      FillStyle       =   0  'Solid
      Height          =   372
      Left            =   12360
      Top             =   7320
      Visible         =   0   'False
      Width           =   156
   End
   Begin VB.Shape cornice_barra_scambio_dati 
      BorderColor     =   &H000000FF&
      Height          =   372
      Left            =   8760
      Top             =   120
      Visible         =   0   'False
      Width           =   2652
   End
End
Attribute VB_Name = "tercm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

'str(numero)=stringa del numero
'str(3)=" 3"
'trim(str(3))="3"
'str(123)="123"
'val("3")=3
'val("123")=123
'asc("0")=48
'chr(48)="0"

' comandi PC->micro->
'     risposte micro->PC
' ## blocca trasmissione (buffer pieno)
' #$ sblocca trasmissione
' #: richiesta stringa di intestazione
'     0xf2, intestazione
'     0xf3, nomi tabelle
'     0xf0, nomi variabili tabella
'     0xf1, variabili tabella
' #. invia i dati della tabella corrente
' #R reset


' #P0..9 punti
' #T0..9 invia tabella 0..26

' #+01..99 incrementa
' #-01..99 decrementa
' #*01..99 doppio click
' #/01..99 doppio click


Option Explicit
Option Base 0

'tabella micri in lista
Const numero_device = 6

Const device1 = "LPC2132"
Const id_device1 = "196369"
Const flash_device1 = 65536
Const settori_device1 = 8
Const ram_adr_device1 = 1073742336
Const vuc_position_device1 = 5
Const uucode1 = 1

Const device2 = "LPC2134"
Const id_device2 = "196370"
Const flash_device2 = 131072
Const settori_device2 = 10
Const ram_adr_device2 = 1073742336
Const vuc_position_device2 = 5
Const uucode2 = 1

Const device3 = "LPC2136"
Const id_device3 = "196387"
Const flash_device3 = 262144
Const settori_device3 = 14
Const ram_adr_device3 = 1073742336
Const vuc_position_device3 = 5
Const uucode3 = 1

Const device4 = "LPC1517"
Const id_device4 = "1517"
Const flash_device4 = 65536
Const settori_device4 = 15
Const ram_adr_device4 = 33555200
Const vuc_position_device4 = 7
Const uucode4 = 0

Const device5 = "LPC1549"
Const id_device5 = "5449"
Const flash_device5 = 262144
Const settori_device5 = 63
Const ram_adr_device5 = 33555200
Const vuc_position_device5 = 7
Const uucode5 = 0

Const device6 = "LPC1114"
Const id_device6 = "440438827"
Const flash_device6 = 32768
Const settori_device6 = 7
Const ram_adr_device6 = 268435456
Const vuc_position_device6 = 7
Const uucode6 = 1

Const device7 = ""
Const id_device7 = ""
Const flash_device7 = 0
Const settori_device7 = 0
Const ram_adr_device7 = 0
Const vuc_position_device7 = 5
Const uucode7 = 0

Const device8 = ""
Const id_device8 = ""
Const flash_device8 = 0
Const settori_device8 = 0
Const ram_adr_device8 = 0
Const vuc_position_device8 = 5
Const uucode8 = 0

Const device9 = ""
Const id_device9 = ""
Const flash_device9 = 0
Const settori_device9 = 0
Const ram_adr_device9 = 0
Const vuc_position_device9 = 5
Const uucode9 = 0

Const device10 = ""
Const id_device10 = ""
Const flash_device10 = 0
Const settori_device10 = 0
Const ram_adr_device10 = 0
Const vuc_position_device10 = 5
Const uucode10 = 0















Dim device, id_device As String
Dim flash_device As Long
Dim settori_device As Integer
Dim ram_adr_device As Long
Dim vuc_position_device As Integer
Dim uucode_device As Integer

Dim dimensione_file As Long

Dim timer_errore_seriale As Integer
Dim fase_comandi, resetta_fase_comandi As Integer
Dim timer_comandi As Integer
Dim cicla As Integer
Dim timer_chiusura_seriale As Integer
Dim numero_tabelle, indice_tabella, tabella_selezionata As Integer
Dim tabella_con_punti(10) As Integer
Dim blocca_ricezione, sblocca_ricezione As Integer
Dim esegue_timer As Integer
Dim comando_interno As String
Dim comando_esterno(50) As String
Dim indice_comando_esterno As Integer
Dim nome_file_hex_con_path, nome_file_hex_senza_path As String
Dim path_file_hex As String
Dim timer_text_report As Integer
Dim timer_programmazione As Integer
Dim salta_caricamento_punto As Boolean
Dim colonna_selezionata, bak_colonna_selezionata As Integer
Dim riga_selezionata, bak_riga_selezionata As Integer


Dim numero_variabili_totale, numero_variabili_parziale As Integer

Dim numero_byte_seriale, numero_stringhe_seriale

Dim aaa, stringa_ricevuta, car As String
Dim contatore, riga, colonna, ii, jj, kk As Integer
Dim portacom As Integer

Dim focus As Integer

Dim processo_download As Long

Dim errore_download As Boolean
Dim errore_comando As Boolean

Const h10000000 = 4294967296#

Dim righe_uu As Integer
Dim rx_cmd, tx_cmd, cmd As String
Dim dato_da_evidenziare(10) As String








' questa costante sono i byte che vengono trasferiti in ram per la scrittura
Const dim_pacchetto = 256



Const fine_variabili = 1


Private Sub Form_Load()
  On Error GoTo qui
  
  numero_variabili_totale = 0
  numero_variabili_parziale = 0
  numero_tabelle = 0
  indice_comando_esterno = 0
  focus = 0
  
  contatore = 0
  riga = 1
  colonna = 0
  win.Col = 0
  win.Row = 0
resize:
  tercm.Height = 10150
  tercm.Width = 11700
  win.ColWidth(0) = 5000
  win.ColWidth(1) = 1700
  win.ColWidth(2) = 30
  win.ColWidth(3) = 700
  win.ColWidth(4) = 700
  win.Width = win.ColWidth(0) + win.ColWidth(1) + win.ColWidth(2) + win.ColWidth(3) + win.ColWidth(4) + 360
  
  seriale.Height = 7572
  
  win.ColAlignment(0) = 1   'sinistra basso
  win.ColAlignment(1) = 4   'centro basso
  win.ColAlignment(2) = 4  'centro basso
  win.ColAlignment(3) = 4  'centro basso
  win.ColAlignment(4) = 4  'centro basso
  
  colonna = 1
  GoTo li

qui:
  tasto_uart.Caption = "ERR"
li:
  
  On Error GoTo qui2
  
  combo_device.AddItem device1
  combo_device.AddItem device2
  combo_device.AddItem device3
  combo_device.AddItem device4
  combo_device.AddItem device5
  If numero_device > 5 Then combo_device.AddItem device6
  If numero_device > 6 Then combo_device.AddItem device7
  If numero_device > 7 Then combo_device.AddItem device8
  If numero_device > 8 Then combo_device.AddItem device9
  If numero_device > 9 Then combo_device.AddItem device10
  
    
  
  'apro il file coi dati di configurazione
  Open App.Path + "\config.txt" For Input As #1
  
  Input #1, riga
  If riga <> "" Then
    If riga = "1" Then
      portacom = 1
    ElseIf riga = "2" Then
      portacom = 2
    ElseIf riga = "3" Then
      portacom = 3
    ElseIf riga = "4" Then
      portacom = 4
    Else
      portacom = 1
    End If
  Else:
    portacom = 1
  End If
  
  Input #1, riga
  If Len(riga) > 0 Then
    combo_device.ListIndex = riga
    'device = riga
    device = combo_device.Text
  Else
    combo_device.ListIndex = Val(riga)
  End If
  
  Input #1, nome_file_hex_con_path
  If nome_file_hex_con_path > "" Then
  
    'tolgo il path per visualizzare solo il nome del file
    Dim tt, ii As Integer
    nome_file_hex_senza_path = nome_file_hex_con_path
    ii = Len(nome_file_hex_senza_path)
    If ii > 0 Then
    
      tt = 1
      While tt > 0
        If Mid(nome_file_hex_senza_path, ii, 1) <> "\" Then
          If ii > 1 Then
            ii = ii - 1
          Else
            tt = 0
          End If
        Else
          ii = ii + 1
          nome_file_hex_senza_path = Mid(nome_file_hex_senza_path, ii, Len(nome_file_hex_senza_path) - ii + 1)
          nome_file_hex_senza_path = Left(nome_file_hex_senza_path, Len(nome_file_hex_senza_path) - 4)
          path_file_hex = Left(nome_file_hex_con_path, ii - 1)
          tt = 0
        End If
      Wend
    
    End If
  
    label_file_hex.Caption = nome_file_hex_senza_path

  End If
  
  Close #1
  GoTo li2

qui2:


li2:
  If portacom < 1 Then portacom = 1
  
  Option2(portacom - 1).Value = True

  carica_dati_device

  


End Sub

Private Sub carica_dati_device()

  If device = device1 Then
    id_device = id_device1
    flash_device = flash_device1
    settori_device = settori_device1
    ram_adr_device = ram_adr_device1
    vuc_position_device = vuc_position_device1
    uucode_device = uucode1
  ElseIf device = device2 Then
    id_device = id_device2
    flash_device = flash_device2
    settori_device = settori_device2
    ram_adr_device = ram_adr_device2
    vuc_position_device = vuc_position_device2
    uucode_device = uucode2
  ElseIf device = device3 Then
    id_device = id_device3
    flash_device = flash_device3
    settori_device = settori_device3
    ram_adr_device = ram_adr_device3
    vuc_position_device = vuc_position_device3
    uucode_device = uucode3
  ElseIf device = device4 Then
    id_device = id_device4
    flash_device = flash_device4
    settori_device = settori_device4
    ram_adr_device = ram_adr_device4
    vuc_position_device = vuc_position_device4
    uucode_device = uucode4
  ElseIf device = device5 Then
    id_device = id_device5
    flash_device = flash_device5
    settori_device = settori_device5
    ram_adr_device = ram_adr_device5
    vuc_position_device = vuc_position_device5
    uucode_device = uucode5
  ElseIf device = device6 Then
    id_device = id_device6
    flash_device = flash_device6
    settori_device = settori_device6
    ram_adr_device = ram_adr_device6
    vuc_position_device = vuc_position_device6
    uucode_device = uucode6
  ElseIf device = device7 Then
    id_device = id_device7
    flash_device = flash_device7
    settori_device = settori_device7
    ram_adr_device = ram_adr_device7
    vuc_position_device = vuc_position_device7
    uucode_device = uucode7
  ElseIf device = device8 Then
    id_device = id_device8
    flash_device = flash_device8
    settori_device = settori_device8
    ram_adr_device = ram_adr_device8
    vuc_position_device = vuc_position_device8
    uucode_device = uucode8
  ElseIf device = device9 Then
    id_device = id_device9
    flash_device = flash_device9
    settori_device = settori_device9
    ram_adr_device = ram_adr_device9
    vuc_position_device = vuc_position_device9
    uucode_device = uucode9
  ElseIf device = device10 Then
    id_device = id_device10
    flash_device = flash_device10
    settori_device = settori_device10
    ram_adr_device = ram_adr_device10
    vuc_position_device = vuc_position_device10
    uucode_device = uucode10
  Else
    text_macchina.Text = "SELECT DEVICE FIRST!!!"
    timer_programmazione = 995
  End If

End Sub



Private Sub Timer1_Timer()
  'ogni 100ms
  
  correzione_timer
  conteggi_timer
  aggiorna_barra_scambio_dati
  aggiorna_finestre_debug
  

  
  

  If timer_programmazione > 0 Then
    
    If clock_1s Then
      
      timer_programmazione = timer_programmazione + 1
    
      If timer_programmazione < 1000 Then
        label_timeout.Visible = True
        If timer_programmazione < 900 Then
          label_timeout.Caption = "Time:" + Str(timer_programmazione)
        End If
      Else
        'ripristino tutto
        tasto_uart.Enabled = True
        frame_com.Enabled = True
        frame_punti.Enabled = True
        frame_tabelle.Enabled = True
        frame_update.Enabled = True
        tasto_update.Caption = "UPDATE"
        tasto_abort.Enabled = False
        tasto_abort.Visible = False
        text_macchina.Visible = False
        text_macchina.Text = "SELECT COM PORT & CLICK START"
        text_report.Visible = False
        tasto_recall_report.Enabled = True
        
        timer_programmazione = 0
        
      End If
    
    End If
    
  End If
  
  


  'stabilisco se la tabella punti è da gestire o meno
  If tabella_con_punti(tabella_selezionata) > 0 Then
    If frame_punti.Visible = False Then
      frame_punti.Visible = True
      salta_caricamento_punto = True
      Option1(0) = 1
    End If
    If Option1(0) = 0 And Option1(1) = 0 And Option1(2) = 0 And Option1(3) = 0 And Option1(4) = 0 And Option1(5) = 0 And Option1(6) = 0 And Option1(7) = 0 And Option1(8) = 0 And Option1(9) = 0 Then Option1(0) = 1
  Else
    frame_punti.Visible = False
  End If

  If tabella_con_punti(tabella_selezionata) > 1 Then
    tasto_debug.Enabled = True
  Else
    tasto_debug.Enabled = False
  End If

  'questo gestisce l'indicazione di porta errata
  If timer_errore_seriale > 1 Then
    timer_errore_seriale = timer_errore_seriale - 1
  ElseIf timer_errore_seriale = 1 Then
    tasto_uart.Caption = "START"
    timer_errore_seriale = 0
  End If


  'visualizzazione finestra text report
  If timer_programmazione Then timer_text_report = 30
  If timer_text_report > 0 Then
    timer_text_report = timer_text_report - 1
  Else
    text_report.Visible = False
  End If


  'gestione per la visualizzazione e gestione dei tasti reset
  If timer_programmazione Then
  ElseIf uart.PortOpen = True Then
    frame_comandi.Enabled = True
    comando_reset(0).Enabled = True
    comando_reset(1).Enabled = True
    frame_com.Enabled = False
  Else
    frame_comandi.Enabled = False
    comando_reset(0).Enabled = False
    comando_reset(1).Enabled = False
    frame_com.Enabled = True
  End If


  'abilitazione tasto programmazione
  If label_file_hex.Caption = "SELECT FILE" Then
    tasto_update.Enabled = False
  ElseIf label_file_hex.Caption = "" Then
    tasto_update.Enabled = False
  Else
    tasto_update.Enabled = True
  End If



  'gestione comandi trasmissione e timeout ricezione risposte
  If timer_programmazione Then
  ElseIf uart.PortOpen = True Then
    
    'gestione delle fasi di trasmissione
    If fase_comandi = 0 Then
      'richiesta versione
      
      text_macchina.Visible = False
      label_timeout.Visible = False
      win.Clear
      seriale.Text = ""
      numero_byte_seriale = 0
      numero_stringhe_seriale = 0
      frame_tabelle.Visible = False
      combo_tabelle.Clear
      stringa_ricevuta = ""
      
      If timer_comandi < 5 Then
        timer_comandi = timer_comandi + 1
      Else
        timer_comandi = 0
        fase_comandi = 1
        comando_interno = "#:"
      End If
    
    ElseIf fase_comandi = 1 Then
      'aspetto ricezione stringa macchina, altrimenti ripeto comando
      
      If timer_comandi < 10 Then
        timer_comandi = timer_comandi + 1
      Else
        timer_comandi = 0
        fase_comandi = 0
      End If
    
    ElseIf fase_comandi = 2 Then
      'se sono qui significa che ho ricevuto risposta al comando precedente
      
      comando_interno = "#0"
      fase_comandi = 3
      timer_comandi = 0
    
    ElseIf fase_comandi = 3 Then
      'aspetto ricezione nomi variabili, altrimenti ripeto comando
      
      If in_ricezione > 0 Then
        timer_comandi = 0
      ElseIf timer_comandi < 10 Then
        timer_comandi = timer_comandi + 1
      Else
        timer_comandi = 0
        fase_comandi = 0
      End If
    
    ElseIf fase_comandi = 4 Then
      'se sono qui significa che ho ricevuto risposta al comando precedente
'debug2 = centesimi - debug1
      comando_interno = "#."
      fase_comandi = 5
      timer_comandi = 0
    
    ElseIf fase_comandi = 5 Then
      'aspetto ricezione valori variabili, altrimenti ripeto comando
      If in_ricezione > 0 Then
        timer_comandi = 0
      ElseIf timer_comandi < 10 Then
        timer_comandi = timer_comandi + 1
      Else
        timer_comandi = 0
        fase_comandi = 0
      End If
    
    Else
      fase_comandi = 0
      timer_comandi = 0
    End If
  
    timer_chiusura_seriale = 10
  
  Else  'seriale chiusa
    
    fase_comandi = 0
    timer_comandi = 0
    
    'visualizza timeout con count down per 10 secondi e poi lo tira via e resetta la finestra dati
    If clock_1s > 0 Then
      If timer_chiusura_seriale > 0 Then
        timer_chiusura_seriale = timer_chiusura_seriale - 1
        label_timeout.Caption = "Timeout: " + Trim(Str(timer_chiusura_seriale))
        label_timeout.Visible = True
        If timer_chiusura_seriale = 0 Then
          win.Clear
          seriale.Text = ""
          numero_byte_seriale = 0
          numero_stringhe_seriale = 0
          frame_tabelle.Visible = False
          combo_tabelle.Clear
        Else
        End If
      Else
        label_timeout.Visible = False
        text_macchina.Text = "SELECT COM PORT & CLICK START"
      End If
    End If
  End If



  'gestione della ricezione

  If timer_programmazione Then
  ElseIf uart.PortOpen = True Then
    
    'leggo i dati dalla seriale
    aaa = uart.Input
    If Len(aaa) > 0 Then
      stringa_ricevuta = stringa_ricevuta + aaa
    End If
  
Dim ll As Integer
  
    ll = Len(stringa_ricevuta)
    'se sono troppo veloce a spedire e la stringa diventa troppo
    'lunga taglio via la parte piu' vecchia
    If ll > 1000 Then
      stringa_ricevuta = Right(stringa_ricevuta, 1000)
      ll = 900
    ElseIf ll > 200 Then
      blocca_ricezione = 1
      sblocca_ricezione = 0
    ElseIf blocca_ricezione Then
      blocca_ricezione = 0
      sblocca_ricezione = 1
    End If
  
        
    ' qui trasmetto cio' che è in attesa, i comandi esterni hanno la precedenza
    If uart.PortOpen = True Then
      If blocca_ricezione Then
        uart.Output = "##"
      ElseIf sblocca_ricezione Then
        uart.Output = "#$"
        sblocca_ricezione = 0
      Else
      
        If comando_esterno(indice_comando_esterno) > "" Then
          'aspetto la fine della ricezione del pacchetto precedente
          If comando_interno = "#." Then
            uart.Output = comando_esterno(indice_comando_esterno)
            comando_esterno(indice_comando_esterno) = ""
            If indice_comando_esterno > 0 Then indice_comando_esterno = indice_comando_esterno - 1
            If resetta_fase_comandi > 0 Then
              fase_comandi = resetta_fase_comandi
              resetta_fase_comandi = 0
              comando_interno = ""
            End If
          End If
        End If
        
        If comando_interno > "" Then
          uart.Output = comando_interno
          comando_interno = ""
  'debug3 = centesimi - debug1
        End If
      End If
    End If
        
        
        
    ll = Len(stringa_ricevuta)
        
            
    'analizzo e sistemo la stringa
    kk = 0
    While kk < ll
    
      'innanzitutto cerco un carattere di inizio stringa (240, 241, 242, 243, 244)
      ii = Asc(Left(stringa_ricevuta, 1))
      If ii = 240 Or ii = 241 Or ii = 242 Or ii = 243 Or ii = 244 Then
        'ho trovato un inizio stringa
          kk = Len(stringa_ricevuta) + 1
      Else
        'se il primo carattere non e' un inizio stringa lo elimino
        stringa_ricevuta = Right(stringa_ricevuta, ll - 1)
        ll = Len(stringa_ricevuta)
      End If
    Wend
  
    'adesso la stringa inizia con un carattere di inizio stringa oppure è rimasta una stringa vuota
  
  
    ll = Len(stringa_ricevuta)
    If ll > 0 Then
      cicla = 1
    Else
      cicla = 0
    End If
    
    
    While cicla > 0
      
      cicla = 0
      
      'prendo il primo carattere e vedo cosa è o sta arrivando
      jj = Asc(Left(stringa_ricevuta, 1))
  
  
      'nomi delle variabili
      If jj = 240 And ll > 1 Then
        
        If Asc(Mid(stringa_ricevuta, 2, 1)) = 255 Then
          'ho trovato l'ultima stringa
  
          If fase_comandi = 3 Then fase_comandi = 4
          stringa_ricevuta = Right(stringa_ricevuta, ll - 2)
          ll = Len(stringa_ricevuta)
          If ll > 0 Then cicla = 1
      
        ElseIf ll > 2 Then
        
          'ho trovato l'inizio di una stringa che contiene il nome della variabile, ne cerco la fine
          'estraggo la posizione
            
          riga = Asc(Mid(stringa_ricevuta, 2, 1))
          'se la posizione è la prima pulisco tutto
          If riga = 0 Then
            win.Clear
            seriale.Text = ""
            numero_byte_seriale = 0
            numero_stringhe_seriale = 0
          
          End If
            
          'faccio un test sulle righe
          If riga > win.Rows - 1 Then riga = win.Rows - 1
            
          colonna = 0
          ii = 3
          aaa = ""
          kk = ll + 1
            
          While ii < ll
            car = Mid(stringa_ricevuta, ii, 1)
            If car = Chr(255) Then
              'ho trovato la fine della stringa, la stampo
              win.Col = 0
              win.Row = riga
              If Right(aaa, 1) = "0" Then
              ElseIf Right(aaa, 1) = "1" Then
                win.Col = 3
                win.Row = riga
                win.Text = "-"
                win.Col = 4
                win.Text = "+"
              ElseIf Right(aaa, 1) = "2" Then
                win.Col = 3
                win.Row = riga
                win.Text = "OFF"
                win.Col = 4
                win.Text = "ON"
              End If
              win.Col = 0
              aaa = Left(aaa, Len(aaa) - 1)
              win.Text = aaa
              If riga = 0 Then
                win.CellFontBold = True
              End If
              stringa_ricevuta = Right(stringa_ricevuta, ll - ii)
              ll = Len(stringa_ricevuta)
              If ll > 0 Then cicla = 1
              ii = ll + 1
              kk = 0
              numero_variabili_totale = riga + 1
              numero_variabili_parziale = 0
              'aggiorna_puntatore
              in_ricezione = 100
                
            Else
              aaa = aaa + car
            End If
            ii = ii + 1
          Wend
        End If
      
      'valori delle variabili
      ElseIf jj = 241 And ll > 1 Then
        
        If Asc(Mid(stringa_ricevuta, 2, 1)) = 255 Then
          'ho trovato l'ultima stringa
          If fase_comandi = 5 Then
            fase_comandi = 4
          End If
          stringa_ricevuta = Right(stringa_ricevuta, ll - 2)
          ll = Len(stringa_ricevuta)
          If ll > 0 Then cicla = 1
        
        ElseIf ll > 2 Then
          'ho trovato l'inizio di una variabile (in formato stringa), ne cerco la fine
          riga = Asc(Mid(stringa_ricevuta, 2, 1))
          If riga > win.Rows Then riga = win.Rows
          
          bak_colonna_selezionata = win.ColSel
          bak_riga_selezionata = win.RowSel
          
          ii = 3
          aaa = ""
          kk = ll + 1
          While ii < ll
            car = Mid(stringa_ricevuta, ii, 1)
            If car = Chr(255) Then
              'ho trovato la fine della stringa, la stampo
              win.Col = 1
              win.Row = riga
              If aaa = "" Then aaa = "0"
              win.Text = aaa
              win.CellFontBold = True
  
              stringa_ricevuta = Right(stringa_ricevuta, ll - ii)
              ll = Len(stringa_ricevuta)
              If ll > 0 Then cicla = 1
              ii = ll + 1
              kk = 0
              in_ricezione = 100
              numero_variabili_parziale = riga + 1
              If numero_variabili_parziale = numero_variabili_totale Then
                If fase_comandi = 5 Then
                  fase_comandi = 4
  'debug1 = centesimi
                End If
                numero_variabili_parziale = 0
              End If
              
              If bak_colonna_selezionata < win.Cols Then win.Col = bak_colonna_selezionata
              If bak_riga_selezionata < win.Rows Then win.Row = bak_riga_selezionata
            Else
              aaa = aaa + car
            End If
            ii = ii + 1
          Wend
        End If
        
      ElseIf jj = 242 And ll > 2 Then
        'ho trovato l'inizio di una stringa che contiene il nome della macchina, ne cerco la fine
        ii = 2
        aaa = ""
        kk = ll + 1
        While ii <= ll
          car = Mid(stringa_ricevuta, ii, 1)
          If car = Chr(255) Then
            'ho trovato la fine della stringa, la stampo
            text_macchina.Text = aaa
            text_macchina.Visible = True
            in_ricezione = 100
            stringa_ricevuta = Right(stringa_ricevuta, ll - ii)
            If fase_comandi = 1 Then fase_comandi = 2
          Else
            aaa = aaa + car
          End If
          
          indice_tabella = 0
          numero_variabili_totale = 0
          numero_variabili_parziale = 0
          
          ii = ii + 1
        Wend
      
      ElseIf jj = 243 And ll > 2 Then
        'ho trovato l'inizio di una stringa che contiene i nomi delle tabelle
        ii = 2
        aaa = ""
        kk = ll + 1
        While ii <= ll
          car = Mid(stringa_ricevuta, ii, 1)
          If car = Chr(255) Then
            Dim indice As Integer
                      
            'ho trovato la fine della stringa, la gestisco
            'estraggo l'indice
            car = Left(aaa, 1)
            'tolgo l'indice
            aaa = Right(aaa, Len(aaa) - 1)
            indice = Asc(car)
            'estraggo la stringa
            If indice >= indice_tabella Then
              indice_tabella = indice_tabella + 1
              frame_tabelle.Visible = True
              combo_tabelle.AddItem Left(aaa, Len(aaa) - 1)
              combo_tabelle.Visible = True
              If indice = 0 Then
                combo_tabelle.ListIndex = 0
                tabella_selezionata = 0
              End If
            End If
            'vedo se la tabella è associata alla gestione dei punti
            car = Right(aaa, 1)
            tabella_con_punti(indice) = Asc(car)
            
            stringa_ricevuta = Right(stringa_ricevuta, ll - ii)
            timer_comandi = 0
            in_ricezione = 100
            
            ll = Len(stringa_ricevuta)
            If ll > 0 Then cicla = 1
            ii = ll + 1
            
          Else
            aaa = aaa + car
          End If
          
          ii = ii + 1
        Wend
      
      ElseIf jj = 244 And ll > 2 Then
        'ho trovato l'inizio di una stringa che contiene una stringa da visualizzare
        'sulla finestra delle stringhe
        
        ii = 2
        aaa = ""
        kk = ll + 1
        While ii <= ll
          car = Mid(stringa_ricevuta, ii, 1)
          If car = Chr(255) Then
            'ho trovato la fine della stringa, la stampo
            seriale.Text = seriale.Text + vbCrLf + aaa
            
            in_ricezione = 100
            stringa_ricevuta = Right(stringa_ricevuta, ll - ii)
          Else
            aaa = aaa + car
          End If
          
          ii = ii + 1
        Wend
          
        numero_byte_seriale = numero_byte_seriale + Len(aaa)
        numero_stringhe_seriale = numero_stringhe_seriale + 1
          
        totale_byte.Text = numero_byte_seriale
        totale_righe.Text = numero_stringhe_seriale
              
      Else
        'fine delle ricerche
        kk = ll + 1
      End If
      
    Wend
  Else
    stringa_ricevuta = ""
  End If

  
'debug1 = fase_comandi
'debug2 = timer_comandi
'debug3 = debug2 - debug1
'deb1.Text = debug1
'deb2.Text = debug2
'deb3.Text = debug3
  
fine_timer_1:
  
End Sub














'serve per interrompere la programmazione
Private Sub tasto_abort_Click()
  timer_programmazione = 1000
End Sub

Private Sub comando_clear_seriale_Click()
  seriale.Text = ""
  totale_byte = ""
  totale_righe = ""
  numero_byte_seriale = 0
  numero_stringhe_seriale = 0
End Sub

Private Sub comando_reset_Click(Index As Integer)
  If Index = 0 Then
  ' devo eseguire un reset, lo faccio hardware
    uart.DTREnable = True
    centesimi = 0
    While centesimi < 10
      DoEvents
    Wend
    uart.DTREnable = False
    fase_comandi = 1
    win.Clear
    seriale.Text = ""
    numero_byte_seriale = 0
    numero_stringhe_seriale = 0
    frame_tabelle.Visible = False
    combo_tabelle.Clear
  ElseIf Index = 1 Then
    If (indice_comando_esterno < 40) Then indice_comando_esterno = indice_comando_esterno + 1
    comando_esterno(indice_comando_esterno) = "#R"
    centesimi = 0
    While centesimi < 10
      DoEvents
    Wend
  End If
    
  focus = Index + 1
  
End Sub





Private Sub label_file_hex_Click()
  CommonDialog1.Filter = "Text files|*.hex"
  CommonDialog1.ShowOpen
  
  Dim file_da_prog As String
  
  file_da_prog = CommonDialog1.FileName
  If Len(file_da_prog) > 4 Then
  
    nome_file_hex_con_path = file_da_prog
    
    'tolgo il path per visualizzare solo il nome del file
    Dim tt, ii As Integer
    nome_file_hex_senza_path = nome_file_hex_con_path
    ii = Len(nome_file_hex_senza_path)
    If ii > 0 Then
    
      tt = 1
      While tt > 0
        If Mid(nome_file_hex_senza_path, ii, 1) <> "\" Then
          If ii > 0 Then
            ii = ii - 1
          Else
            tt = 0
          End If
        Else
          ii = ii + 1
          nome_file_hex_senza_path = Mid(nome_file_hex_senza_path, ii, Len(nome_file_hex_senza_path) - ii + 1)
          nome_file_hex_senza_path = Left(nome_file_hex_senza_path, Len(nome_file_hex_senza_path) - 4)
          path_file_hex = Left(nome_file_hex_con_path, ii - 1)
          tt = 0
        End If
      Wend
    
    End If
    label_file_hex.Caption = nome_file_hex_senza_path
  End If
End Sub


'sono i punti da caricare
Private Sub Option1_Click(Index As Integer)
  If salta_caricamento_punto Then
    salta_caricamento_punto = False
  Else
    If (indice_comando_esterno < 40) Then indice_comando_esterno = indice_comando_esterno + 1
    comando_esterno(indice_comando_esterno) = "#T" + Chr(Asc("0") + Index)
  End If
End Sub

Private Sub Option2_Click(Index As Integer)
   portacom = Index + 1
End Sub


Private Sub tasto_debug_Click()
  If tercm.Width = 17300 Then
    tercm.Width = 11700
    tasto_debug.Caption = "->"
  Else
    tercm.Width = 17300
    tasto_debug.Caption = "<-"
  End If
  
  If focus = 0 Then
    tasto_uart.SetFocus
  ElseIf focus = 1 Then
    comando_reset(0).SetFocus
  ElseIf focus = 2 Then
    comando_reset(1).SetFocus
  Else
    focus = 0
    tasto_uart.SetFocus
  End If
  

End Sub

Private Sub tasto_extra_Click()
'stampo la riga

End Sub

Private Sub tasto_recall_report_Click()
  If text_report.Visible = True Then
    text_report.Visible = False
    timer_text_report = 0
  Else
    text_report.Visible = True
    timer_text_report = 50
  End If
End Sub

'cambio tabella
Private Sub tasto_selezione_tabella_Click()
  If (indice_comando_esterno < 40) Then indice_comando_esterno = indice_comando_esterno + 1
  comando_esterno(indice_comando_esterno) = "#" + Trim(Str(combo_tabelle.ListIndex))
  tabella_selezionata = combo_tabelle.ListIndex
  resetta_fase_comandi = 3
End Sub

Private Sub tasto_uart_Click()
  On Error GoTo seriale_occupata
  If uart.PortOpen = False Then
    apri_seriale
    tasto_uart.Caption = "STOP"
    cornice_barra_scambio_dati.Visible = True
    posizione_puntatore_barra_scambio_dati = cornice_barra_scambio_dati.Left
    verso_puntatore_barra_scambio_dati = 1
    puntatore.Left = posizione_puntatore_barra_scambio_dati
    puntatore.Top = cornice_barra_scambio_dati.Top
    puntatore.Visible = True
'    tasto_extra.Visible = True
'    comando(0).Visible = False
  Else
    chiudi_seriale
    tasto_uart.Caption = "START"
    cornice_barra_scambio_dati.Visible = False
    puntatore.Visible = False
'    tasto_extra.Visible = False
'    comando(0).Visible = True
  End If
  GoTo fine_tasto_uart
  
seriale_occupata:
  tasto_uart.Caption = "COMM ERROR"
  timer_errore_seriale = 30
fine_tasto_uart:

  focus = 0
  
End Sub

Private Sub tasto_exit_Click()
  If uart.PortOpen = True Then
    chiudi_seriale
  End If
  
  
  On Error GoTo qui
  Close
  
  Open App.Path + "\config.txt" For Output As #1
  If portacom = 1 Then
    Print #1, "1"
  ElseIf portacom = 2 Then
    Print #1, "2"
  ElseIf portacom = 3 Then
    Print #1, "3"
  ElseIf portacom = 4 Then
    Print #1, "4"
  Else
    Print #1, "1"
  End If
  
  If combo_device.ListIndex = -1 Then
    If combo_device.Text <> "" Then
      Print #1, combo_device.Text
    Else
      Print #1, Str(combo_device.ListIndex)
    End If
  Else
    Print #1, Str(combo_device.ListIndex)
  End If
  
  'salvo il nome file
  If nome_file_hex_con_path > "" Then Print #1, nome_file_hex_con_path
  
  Close #1
qui:
  End
End Sub

Private Sub tasto_update_Click()
  
Dim stato_seriale As Boolean
 
  errore_download = False
  errore_comando = False
  
  'blocco il tasto fino alla fine
  tasto_update.Enabled = False
  
  'leggo lo stato della porta per ripristinarlo alla fine e se è aperta la chiudo
  If uart.PortOpen = True Then
    stato_seriale = True
    chiudi_seriale
    'inserisco una pausa
    centesimi = 0
    While centesimi < 10
      DoEvents
    Wend
  Else
    stato_seriale = False
  End If
    
  cornice_barra_scambio_dati.Visible = False
  text_macchina.Visible = False
  puntatore.Visible = False
  
  On Error Resume Next
    
  timer_programmazione = 1
    
    
  tasto_uart.Enabled = False
  frame_com.Enabled = False
  frame_punti.Enabled = False
  frame_tabelle.Enabled = False
  frame_update.Enabled = False
  tasto_update.Caption = "prog..."
  tasto_abort.Enabled = True
  tasto_abort.Visible = True
  text_macchina.Visible = True
    
  If combo_device.ListIndex >= 0 Then
    device = combo_device.Text
  End If
    
  'faccio delle verifiche!!!
  If device = device1 Then
  ElseIf device = device2 Then
  ElseIf device = device3 Then
  ElseIf device = device4 Then
  ElseIf device = device5 Then
  ElseIf device = device6 Then
  ElseIf device = device7 Then
  ElseIf device = device8 Then
  ElseIf device = device9 Then
  ElseIf device = device10 Then
  Else
    text_macchina.Text = "SELECT DEVICE FIRST!!!"
    timer_programmazione = 995
    GoTo fine_tasto_update
  End If
    
    
  If path_file_hex = "" Or nome_file_hex_senza_path = "" Then
    MsgBox "File non specificato o inesistene", vbCritical + vbOKOnly, "Errore!"
    timer_programmazione = 995
    GoTo fine_tasto_update
  End If
          
  'inizio il download e apro la finestra di report
  text_report.Text = ""
  text_report.Visible = True
          
  On Error GoTo err_update

  tasto_update.Caption = "Download..."

  'inizio preparando il file
  
  'come prima cosa estraggo dal file hex il solo codice
  estrai_codice_hex
  If errore_download Then GoTo err_update


  'poi calcolo il vuc e lo metto al posto giusto
  carica_vuc
  If errore_download Then GoTo err_update
  
  prepara_file_download
  If errore_download Then GoTo err_update
'GoTo fine_update

  
  'inizio aprendo la porta
  apri_seriale
  
  resetta_micro
  
  metti_il_micro_in_isp_mode
  If errore_download Then GoTo err_update
  
  sincronizza_micro
  If errore_download Then GoTo err_update
  
  
  leggi_id
  If errore_download Then GoTo err_update
  
  unlock_micro
  If errore_download Then GoTo err_update
    
  ' queste le ho usate per decodificare la uu_encode
'leggi_flash
'If errore_comando = True Then GoTo err_update
'decodifica_flash
'GoTo fine_update
  
  cancella_flash
  If errore_download Then GoTo err_update
  
  resetta_micro
  If errore_download Then GoTo err_update
  
  metti_il_micro_in_isp_mode
  If errore_download Then GoTo err_update
  
  sincronizza_micro
  If errore_download Then GoTo err_update
  
  check_blank
  If errore_download Then GoTo err_update
  
  unlock_micro
  If errore_download Then GoTo err_update
  
  scarica_programma
  If errore_download Then GoTo err_update
  
  resetta_micro
  
  chiudi_seriale


  If stato_seriale = True Then
    apri_seriale
  End If




  tasto_update.Caption = "UPDATE OK!"
  
  text_report.Text = text_report.Text + "UPDATE OK!"
  text_report.SelStart = InStr(text_report.Text, "UPDATE OK!") - 1
  text_report.SelLength = Len("UPDATE OK!")
  text_report.SelBold = True
  text_report.SelColor = vbGreen
  
  timer_programmazione = 995
  GoTo fine_tasto_update

err_update:
  timer_programmazione = 995
  
  On Error GoTo fine_tasto_update
  If InStr(text_report.Text, "ERROR") > 0 Then
    text_report.SelStart = InStr(text_report.Text, "ERROR") - 1
    text_report.SelLength = Len("ERROR")
    text_report.SelBold = True
    text_report.SelColor = vbRed
  End If
  
  GoTo fine_tasto_update
    
fine_tasto_update:

End Sub


Private Sub combo_device_LostFocus()
  device = combo_device.Text
  carica_dati_device
End Sub


Private Sub text_report_Click()
  text_report.Visible = False
End Sub







Private Sub win_Click()

  colonna_selezionata = win.ColSel
  riga_selezionata = win.RowSel
  
  If uart.PortOpen = True And fase_comandi > 3 Then
    
    If (indice_comando_esterno < 40) Then
      'solo se non sono intasato
      indice_comando_esterno = indice_comando_esterno + 1
    
      If colonna_selezionata = 3 Then
        'trasmetto codice decremento
        If riga_selezionata <= 25 Then
          'questo è compatibile con le versioni vecchie
           comando_esterno(indice_comando_esterno) = "#" + Chr(Asc("a") + riga_selezionata)
        Else
          'questo funziona con le versioni nuove e mi permette di gestire le variabili con indice maggiore di 26
          comando_esterno(indice_comando_esterno) = "#-" + Trim(Str(riga_selezionata))
        End If
            
      ElseIf colonna_selezionata = 4 Then
        'trasmetto codice incremento
        
        If riga_selezionata <= 25 Then
          'questo è compatibile con le versioni vecchie
           comando_esterno(indice_comando_esterno) = "#" + Chr(Asc("A") + riga_selezionata)
        Else
          'questo funziona con le versioni nuove e mi permette di gestire le variabili con indice maggiore di 26
          comando_esterno(indice_comando_esterno) = "#+" + Trim(Str(riga_selezionata))
        End If
      End If
        
      bak_colonna_selezionata = colonna_selezionata
      bak_riga_selezionata = riga_selezionata
      
    End If
  
  End If
  
  If focus = 0 Then
    tasto_uart.SetFocus
  ElseIf focus = 1 Then
    comando_reset(0).SetFocus
  ElseIf focus = 2 Then
    comando_reset(1).SetFocus
  Else
    focus = 0
    tasto_uart.SetFocus
  End If

End Sub

Private Sub win_DblClick()
  win_Click
End Sub



Public Sub apri_seriale()
  If uart.PortOpen = False Then
    uart.CommPort = portacom
    uart.Settings = "19200,n,8,1"
    uart.DTREnable = False
    uart.RTSEnable = False
    uart.EOFEnable = False
    uart.Handshaking = comNone
    uart.InBufferSize = 1024
    uart.InputMode = comInputModeText
    uart.InputLen = 0
    uart.RThreshold = 100
    uart.SThreshold = 100
    uart.PortOpen = True
  End If
End Sub

Public Sub chiudi_seriale()
  If uart.PortOpen = True Then
    uart.PortOpen = False
  End If
End Sub



























































Private Sub estrai_codice_hex()

Dim conta_riga As Long
Dim indirizzo_hex As Long
Dim dim_riga As Integer
Dim adr_riga As Long
Dim tipo_riga As Integer
Dim chk, chk_riga As Integer
Dim extra_address As Long
Dim riga_in, riga_out As String

  text_report.Text = text_report.Text + "Extract code from file...." + vbLf
  
  'apro il file
  Open nome_file_hex_con_path For Input As #1
  Open path_file_hex + "file_solo_codice.txt" For Output As #2
  conta_riga = 0
  indirizzo_hex = 0
  extra_address = 0
  riga_out = ""
  
loop_hex:
  If EOF(1) Then
    GoTo end_loop_hex
  End If
  
  Input #1, riga_in
  
'If conta_riga = 2049 Then
'  tasto_update.Caption = conta_riga
'End If
  
  If Len(riga_in) < 8 Then
    GoTo errore_riga_hex
  End If
  If Mid(riga_in, 1, 1) <> ":" Then
    GoTo errore_riga_hex
  End If
  dim_riga = dec(Mid(riga_in, 2, 2))
  adr_riga = Val(dec(Mid(riga_in, 4, 4))) + extra_address

'If adr_riga = 11456 Then
'  nop
'End If

  tipo_riga = Val(Mid(riga_in, 8, 2))
  conta_riga = conta_riga + 1
  




'struttura di un file hex, spiegazione dei byte per ogni riga:
'1: carattere di start, deve essere ":"
'2: indica il numero di byte della riga
'3,4: indirizzo
'5: record type
' 0-dati
' 1-eof
' 2-extended segment address
' 3-start segment address
' 4-extended linear address
' 5-start linear address
'6....: dati
'ultimo: checksum, complemento a 2 della somma di tutti i byte dopo il :

  If tipo_riga = 1 Then
    GoTo tipo_riga_1
  ElseIf tipo_riga = 2 Then
    GoTo tipo_riga_2
  ElseIf tipo_riga = 3 Then
    GoTo tipo_riga_3
  ElseIf tipo_riga = 4 Then
    GoTo tipo_riga_4
  ElseIf tipo_riga = 5 Then
    GoTo tipo_riga_5
  End If
  
tipo_riga_0:  'riga che contiene dati da trasmettere
  'verifico la lunghezza della riga
  If dim_riga > 16 Then
    GoTo errore_riga_hex
  End If
  If Len(riga_in) <> 11 + dim_riga * 2 Then
    GoTo errore_riga_hex
  End If
  'lunghezza ok, verifico chk
  
  'calcolo il chk della riga
  chk = 0
  For ii = 2 To Len(riga_in) - 3 Step 2
    chk = chk + dec(Mid(riga_in, ii, 2))
    If chk > 255 Then chk = chk - 256
  Next
  
  'lo complemento
  If chk > 0 Then
    chk = 256 - chk
  End If
    
  'estraggo il chk della riga
  chk_riga = dec(Right(riga_in, 2))
  'lo confronto
  If chk <> chk_riga Then
    GoTo errore_riga_hex
  End If
  
  'la riga è giusta, estraggo i dati
  riga_out = riga_out + Mid(riga_in, 10, dim_riga * 2)
  indirizzo_hex = indirizzo_hex + dim_riga
  
  
'  While dim_riga < 16
'    riga = riga + "FF"
'    dim_riga = dim_riga + 1
'    indirizzo_hex = indirizzo_hex + 1
'  Wend
  
  If Len(riga_out) >= 32 Then
    Print #2, Left(riga_out, 32)
    riga_out = Right(riga_out, Len(riga_out) - 32)
  End If
  GoTo loop_hex
  
tipo_riga_1:  'riga di fine file
  
  'completo con FF fino ad arrivare a multiplo di 256
  While indirizzo_hex Mod (4096) > 0
    riga_out = riga_out + "FF"
    If Len(riga_out) >= 32 Then
      Print #2, Left(riga_out, 32)
      riga_out = Right(riga_out, Len(riga_out) - 32)
    End If
    indirizzo_hex = indirizzo_hex + 1
  Wend
  
  
  If Len(riga_out) > 0 Then GoTo errore_riga_hex
  dimensione_file = indirizzo_hex
  text_report.Text = text_report.Text + "file is " + Trim(Str(dimensione_file)) + " byte long." + vbLf

  Print #2, ""

  If indirizzo_hex >= flash_device Then
    errore_download = True
    text_report.Text = text_report.Text + "ERROR: file is too long for device!" + vbLf
  End If
  
  GoTo end_loop_hex

tipo_riga_2:
tipo_riga_3:
  GoTo loop_hex
tipo_riga_4:  'riga che contiene indirizzo esteso del file hex dul byte di dato
  
  extra_address = dec(Mid(riga_in, 10, 4)) * 65536
  adr_riga = adr_riga + extra_address
  If indirizzo_hex > adr_riga Then
    GoTo errore_riga_hex
  ElseIf indirizzo_hex < adr_riga Then
    While indirizzo_hex < adr_riga
      riga_out = riga_out + "FF"
      indirizzo_hex = indirizzo_hex + 1
      If Len(riga_out) >= 32 Then
        Print #2, Left(riga_out, 32)
        riga_out = Right(riga_out, Len(riga_out) - 32)
      End If
    Wend
  End If
    
  indirizzo_hex = adr_riga
tipo_riga_5:  'riga iniziale
  GoTo loop_hex
  
errore_riga_hex:
    
  text_report.Text = text_report.Text + "File is not good!" + vbLf
  errore_download = True
  tasto_update.Caption = "ERROR"

end_loop_hex:

  Close #1
  Close #2
  

End Sub



Private Sub carica_vuc()

Dim aa As String
Dim ii As Integer

Dim riga1, riga2, riga3 As String
Dim vect, vuc As Double
Dim strvuc As String
Dim cont As Integer

  On Error GoTo errore_vuc



  
  
  
  'devo aggiungere il Valid User Code all'indirizzo 0x14
  'il VUC è il complemento a 2 degli altri vettori di interrupt,
  'quindi sommo i long da 0x00 a 0x1c (escluso 14), faccio il cpl a 2
  'e lo metto in 0x14

On Error GoTo errore_vuc


  text_report.Text = text_report.Text + "Prepare file for download..." + vbLf

  Open path_file_hex + "file_solo_codice.txt" For Input As #1
  Open path_file_hex + "file_codice_con_vuc.txt" For Output As #2
  
  Line Input #1, riga1
  Line Input #1, riga2
  
  vuc = 0
  cont = 0
  riga3 = riga1 + riga2
loop_vuc:
  
  'little endian, ocio che sono al contrario (LSB first)
  vect = dec(Mid(riga3, cont + 7, 2))
  vect = vect * 256 + dec(Mid(riga3, cont + 5, 2))
  vect = vect * 256 + dec(Mid(riga3, cont + 3, 2))
  vect = vect * 256 + dec(Mid(riga3, cont + 1, 2))
  
  vuc = vuc + vect
  If vuc >= h10000000 Then
    vuc = vuc - h10000000
  End If
  
  cont = cont + 8
  If cont = vuc_position_device * 8 Then
    cont = vuc_position_device * 8 + 8
  End If
  
  If cont < 60 Then GoTo loop_vuc
    
  
  'devo fare il complemento a 2
  If vuc > 0 Then
    vuc = h10000000 - vuc
  End If

'  'nella riga 2 inserisco il vuc
  strvuc = hex(vuc)
  If Len(strvuc) > 8 Then
    GoTo errore_vuc
  Else
    While Len(strvuc) < 8
      strvuc = "0" + strvuc
    Wend
  End If
  
  'giro la stringa per mettere a posto l'ordine dei byte
  cont = vuc_position_device * 8
  cont = cont - 32
  Mid(riga2, cont + 1, 2) = Mid(strvuc, 7, 2)
  Mid(riga2, cont + 3, 2) = Mid(strvuc, 5, 2)
  Mid(riga2, cont + 5, 2) = Mid(strvuc, 3, 2)
  Mid(riga2, cont + 7, 2) = Mid(strvuc, 1, 2)
  
  Print #2, riga1
  Print #2, riga2
  
  'ora ricopio tutto il resto pari pari
loop_2_vuc:
  If EOF(1) Then
    GoTo end_vuc
  End If
  
  Input #1, riga3
  Print #2, riga3
  GoTo loop_2_vuc
  
errore_vuc:
  text_report.Text = text_report.Text + "VUC Error!" + vbLf
  errore_download = True
  tasto_update.Caption = "errore vuc"
  GoTo fine_vuc
  
end_vuc:
    
fine_vuc:
  Close #1
  Close #2
  
End Sub

  
Private Sub prepara_file_download()


  If uucode_device = 1 Then
    prepara_file_uu
  End If
End Sub


Private Sub prepara_file_uu()

  'preparo il file con le righe già pronte da 256 byte alla volta
  'quindi avrò pacchetti da 5 righe complete, una riga non completa e un chk
  
  'adesso devo convertire le stringhe binarie in uucode
  'uucode converte 3 byte binari in 4 byte di caratteri ascii stampabili
  'prendo 45 caratteri e li trasformo in 60 creando una riga, in testa alla riga
  'aggiungo il numero di caratteri originali (45) e aggiungo 32, 45+32=77="M"
  'si creano così righe da 61 caratteri,
  'inoltre bisogna aggiungere un checksum ogni 20 righe convertite
  'il checksum è la somma dei byte prima della conversione e si invia in
  'decimale e completa
  'ad ogni checksum inviato il bootloader risponde "OK<cr><lf>" o
  '"RESEND<cr><lf>" se il checksum è sbagliato
 
  'prendo 3 byte e li spezzo in 4 byte da 6 bit ciascuno,
  'poi aggiungo 32 ad ogni byte in modo che ogni byte risultante è
  'compreso tra 32 e 32+63=95
   
Dim num_righe As Long
Dim chk, chk_righe As Long
Dim num_car As Integer
Dim tx As String
Dim b1, b2, b3 As Integer
Dim c1, c2, c3, c4 As Integer

Dim righe_complete As Integer
Dim caratteri_ultima_riga As Integer
Dim ultime_terne As Integer
Dim caratteri_ultima_terna As Integer
Dim caratteri_ultimi_pacchetti
   
   
  On Error GoTo err_encode
  
  
  righe_complete = Int(dim_pacchetto / 45)
  caratteri_ultima_riga = dim_pacchetto - righe_complete * 45
  ultime_terne = Int(caratteri_ultima_riga / 3)
  caratteri_ultima_terna = caratteri_ultima_riga - ultime_terne * 3
  caratteri_ultimi_pacchetti = Int(caratteri_ultima_riga / 3) * 3 + 3
 
  righe_uu = righe_complete + 1
 
  Open path_file_hex + "file_codice_con_vuc.txt" For Input As #1
  Open path_file_hex + "file_codice_uu_encode.txt" For Output As #2


loop_encode:
  num_righe = 0
  chk_righe = 0
  num_car = 0
  tx = ""
  riga = ""
  
encode_prendi_riga:
  
  If EOF(1) Then
    GoTo ultime_fasi_encode
  End If
  
  'prendo una riga
  Line Input #1, aaa
  riga = riga + aaa
  
  'prendo 3 caratteri e li codifico
  While Len(riga) >= 6
    
    If num_righe = righe_complete And num_car = Int(caratteri_ultima_riga / 3) * 3 Then
    
      aaa = Left(riga, 2)
      aaa = aaa + aaa + aaa
      'tolgo i 3 caratteri dalla riga
      riga = Right(riga, Len(riga) - 2)
      b1 = dec(Mid(aaa, 1, 2))
      b2 = dec(Mid(aaa, 3, 2))
      b3 = dec(Mid(aaa, 5, 2))
      chk = chk + b1
      
    Else
      
      aaa = Left(riga, 6)
      'tolgo i 3 caratteri dalla riga
      riga = Right(riga, Len(riga) - 6)
      b1 = dec(Mid(aaa, 1, 2))
      b2 = dec(Mid(aaa, 3, 2))
      b3 = dec(Mid(aaa, 5, 2))
      chk = chk + b1 + b2 + b3
      
    End If
    
    
    c1 = Int(b1 / 4)
    c2 = (b1 Mod 4) * 16 + Int(b2 / 16)
    c3 = (b2 Mod 16) * 4 + Int(b3 / 64)
    c4 = b3 Mod 64
    
    'sommo 32 ai 4 caratteri ottenuti
    If c1 > 0 Then
      c1 = c1 + 32
    Else
      c1 = 64 + 32
    End If
    
    If c2 > 0 Then
      c2 = c2 + 32
    Else
      c2 = 64 + 32
    End If
    
    If c3 > 0 Then
      c3 = c3 + 32
    Else
      c3 = 64 + 32
    End If
    
    If c4 > 0 Then
      c4 = c4 + 32
    Else
      c4 = 64 + 32
    End If
    
    tx = tx + Chr(c1) + Chr(c2) + Chr(c3) + Chr(c4)
    
    num_car = num_car + 3
    
    'scrivo righe complete e l'ultima incompleta
    
    If num_righe = righe_complete Then
      If num_car = caratteri_ultimi_pacchetti Then
        num_car = caratteri_ultima_riga + 32
        tx = Chr(num_car) + tx
        Print #2, tx
        Print #2, Trim(chk)
        tx = ""
        num_car = 0
        num_righe = 0
        chk = 0
      End If
    Else
        
      If num_car = 45 Then
        
        num_car = num_car + 32
        tx = Chr(num_car) + tx
        Print #2, tx
        tx = ""
        num_righe = num_righe + 1
        num_car = 0
        
        'ogni 20 righe scrivo il checksum
        If num_righe = 20 Then
          Print #2, Trim(chk)
          chk = 0
          num_righe = 0
        End If
        
      End If
    End If
    
  Wend
    
  GoTo encode_prendi_riga
  
err_encode:
  text_report.Text = text_report.Text + "UU-Encode Error!" + vbLf
  errore_download = True
  
ultime_fasi_encode:
  
  'vedo se la riga è terminata
  
  If Len(riga) > 0 Then
    
    If Len(riga) >= 6 Then
      GoTo err_encode
    End If
    
    'codifico l'ultima terna
    If Len(riga) = 2 Then
      aaa = riga + riga + riga
      b1 = dec(Mid(aaa, 1, 2))
      b2 = dec(Mid(aaa, 3, 2))
      b3 = dec(Mid(aaa, 5, 2))
      chk = chk + b1
      num_car = num_car + 1
    ElseIf Len(riga) = 4 Then
      aaa = riga + Left(riga, 2)
      b1 = dec(Mid(aaa, 1, 2))
      b2 = dec(Mid(aaa, 3, 2))
      b3 = dec(Mid(aaa, 5, 2))
      chk = chk + b1 + b2
      num_car = num_car + 2
    Else
      GoTo err_encode
    End If
    
    c1 = Int(b1 / 4)
    c2 = (b1 Mod 4) * 16 + Int(b2 / 16)
    c3 = (b2 Mod 16) * 4 + Int(b3 / 64)
    c4 = b3 Mod 64
    
    'sommo 32 ai 4 caratteri ottenuti
    c1 = c1 + 32
    c2 = c2 + 32
    c3 = c3 + 32
    c4 = c4 + 32
    
    tx = tx + Chr(c1) + Chr(c2) + Chr(c3) + Chr(c4)
    
    
    If num_car = 45 Then
      num_car = num_car + 32
      tx = Chr(num_car) + tx
      Print #2, tx
      tx = ""
      num_righe = num_righe + 1
      num_car = 0
      
      'ogni 20 righe scrivo il checksum
      If num_righe = 20 Then
        Print #2, Trim(chk)
        chk = 0
        num_righe = 0
      End If
      
    Else
      'stampo la riga incompleta
      
      num_car = num_car + 32
      tx = Chr(num_car) + tx
      Print #2, tx
      tx = ""
      num_righe = num_righe + 1
      num_car = 0
          
    End If
    
    
    
  End If
  
  If num_righe > 0 Then
  'alla fine stampo comunque il checksum
    Print #2, Trim(chk)
    chk = 0
    num_righe = 0
  End If
  
  Print #2, "end file"
  
fine_encode:
  Close #1
  Close #2
  
  
End Sub




Private Sub resetta_micro()

  'metto il micro in reset
  uart.DTREnable = True
  centesimi = 0
  While centesimi < 10
    DoEvents
  Wend
    
  text_report.Text = text_report.Text + "Reset MicroPropcessor..." + vbLf
    

tasto_update.Caption = "ISP MODE"
  'metto il micro in run
  uart.RTSEnable = False
  centesimi = 0
  While centesimi < 10
    DoEvents
  Wend
  
  'tolgo il reset
  uart.DTREnable = False
  centesimi = 0
  While centesimi < 10
    DoEvents
  Wend

End Sub



Private Sub metti_il_micro_in_isp_mode()
  
  'metto il micro in reset
  uart.DTREnable = True
  centesimi = 0
  While centesimi < 10
    DoEvents
  Wend
    
    

  tasto_update.Caption = "ISP MODE"
  'metto il micro in ISP
  uart.RTSEnable = True
  centesimi = 0
  While centesimi < 10
    DoEvents
  Wend
  
  'tolgo il reset
  uart.DTREnable = False
  centesimi = 0
  While centesimi < 10
    DoEvents
  Wend

End Sub


Private Sub sincronizza_micro()
  Dim rx As String
  Dim prove As Integer
  prove = 0

  text_report.Text = text_report.Text + "Connect to MicroProcessor..." + vbLf

  'invio il 0x3f di sincronizzazione
  tasto_update.Caption = "SYNCRO"

  'svuoto buffer di ricezione per sicurezza
  rx = uart.Input

invia_punto_interrogativo:
  invia_comando (Chr(Asc("?")))
  attendi_risposta ("Synchronized" + vbCr + vbLf)
  
  If errore_comando = True Then
    If prove < 10 Then
      prove = prove + 1
      GoTo invia_punto_interrogativo
    Else
      GoTo err_sincro
    End If
  End If
  invia_comando ("Synchronized" + Chr(13) + Chr(10))
  attendi_risposta ("Synchronized" + vbCr + vbLf + "OK" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_sincro
  
  
  'invio la frequenza dell'oscillatore
  tasto_update.Caption = "SET FREQ."
  invia_comando ("12000" + vbCr + vbLf)
  attendi_risposta ("12000" + vbCr + vbLf + "OK" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_sincro
  
  errore_comando = False
  GoTo fine_sincro
  
err_sincro:
  text_report.Text = text_report.Text + "ERROR: fail to connect!" + vbLf
  errore_download = True
  
fine_sincro:
  End Sub
  


Private Sub cancella_flash()

  On Error GoTo err_delete_flash

  text_report.Text = text_report.Text + "Delete old version..." + vbLf

  tasto_update.Caption = "PREPARE"
  
  'prepare for erase
  cmd = "P 0 " + Trim(Str(settori_device))
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_delete_flash
  
  tasto_update.Caption = "ERASE"
  'erase
  
  cmd = "E 0 " + Trim(Str(settori_device))
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_delete_flash

  GoTo fine_delete_flash
  
err_delete_flash:
  errore_download = True
  tasto_update.Caption = "ERR.DELE"
  text_report.Text = text_report.Text + "ERROR: can't erase device!"
fine_delete_flash:

End Sub



Private Sub check_blank()
  
  On Error GoTo err_check_blank

  text_report.Text = text_report.Text + "Blank verify..."
  
  tasto_update.Caption = "CHECK BLANK"
  cmd = "I 1 " + Trim(Str(settori_device))
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_check_blank

  text_report.Text = text_report.Text + "OK" + vbLf
  GoTo fine_check_blank
  
err_check_blank:
  text_report.Text = text_report.Text + "ERROR: device is not blank!"
  errore_download = True
  tasto_update.Caption = "ERR.BLANK"

fine_check_blank:


End Sub



Private Sub leggi_id()

  text_report.Text = text_report.Text + "ID Verify..."

  'leggo il part ID
  tasto_update.Caption = "READ ID"
  invia_comando ("J" + vbCr + vbLf)
  attendi_risposta ("J" + vbCr + vbLf + "0" + vbCr + vbLf + id_device + vbCr + vbLf)

  If errore_comando = True Then
    errore_download = True
    text_report.Text = text_report.Text + "ERROR" + vbLf
  Else
    text_report.Text = text_report.Text + "OK" + vbLf
  End If

End Sub





Private Sub unlock_micro()

  'unlock
  text_report.Text = text_report.Text + "Unlock MicroProcessor" + vbLf
  tasto_update.Caption = "UNLOCK"
  invia_comando ("U 23130" + vbCr + vbLf)
  attendi_risposta ("U 23130" + vbCr + vbLf + "0" + vbCr + vbLf)
  
  If errore_comando = True Then errore_download = True

End Sub
  


Private Sub leggi_flash()
  
  On Error GoTo err_read_flash
  
  
  Dim conta_righe_rx As Integer
  Dim byte_da_leggere As Integer
  
  text_report.Text = text_report.Text + "Read Flash..." + vbLf
  
  Open path_file_hex + "file_read_flash.uuc" For Output As #1
  
  'leggo la flash e la salvo in un file
  cmd = "R 256 4"
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_read_flash
  
  'pulisco la riga
  rx_cmd = Right(rx_cmd, Len(rx_cmd) - Len(cmd + vbCr + vbLf + "0" + vbCr + vbLf))
  
  'adesso mi arrivano i dati
  conta_righe_rx = 0
  byte_da_leggere = Int(256 / 3)
  If Int(256 / 3) < 256 / 3 Then byte_da_leggere = byte_da_leggere + 1
  byte_da_leggere = byte_da_leggere * 4
  byte_da_leggere = byte_da_leggere + Int(byte_da_leggere / 60)
  If Int(256 / 3) < 256 / 3 Then byte_da_leggere = byte_da_leggere + 1
  
  

loop_ricevi_righe:
  centesimi = 0
  While centesimi < 100
    DoEvents
    aaa = uart.Input
    If Len(aaa) > 0 Then
      rx_cmd = rx_cmd + aaa
      If Len(rx_cmd) >= byte_da_leggere Then centesimi = 1000
    End If
  Wend
  
  Print #1, rx_cmd
  byte_da_leggere = byte_da_leggere - Len(rx_cmd)
  
  If byte_da_leggere > 0 Then
    invia_comando ("OK" + vbCr + vbLf)
    GoTo loop_ricevi_righe
  End If
  
  GoTo fine_read_flash
  
err_read_flash:
  errore_download = True
  
fine_read_flash:
  
  Close #1
  
End Sub


Private Sub scarica_programma()

  If uucode_device = 1 Then
    scarica_programma_uu
  Else
    scarica_programma_bin
  End If
  
End Sub




Private Sub scarica_programma_uu()

  Dim righe(25) As String
  Dim punta_riga As Integer
  Dim tentativi As Integer

  Dim flash As Long

  On Error GoTo err_write_flash

  'è tutto pronto, devo solo inviare le righe

  'cambio frequenza per andare + veloce
  cmd = "B 38400 1"
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_write_flash

  uart.Settings = "38400,n,8,1"

  'aspetto un attimo e svuoto la seriale
  centesimi = 0
  While centesimi < 50
    DoEvents
  Wend
  aaa = uart.Input
  
  'ora il micro è cancellato, inizio il download del nuovo firmware
inizio_download_file:
  
  Open path_file_hex + "file_codice_uu_encode.txt" For Input As #1
 
  text_report.Text = text_report.Text + "Download new version..." + vbLf
  
  
'per scrivere devo trasferire le righe in ram partendo dall'indirizzo
'0x40000200 che in decimale corrisponde a 107374336
'scrivo 256 byte alla volta
  
'le righe sono tutte pronte per la trasmissione
'ogni riga contiene 45 byte
'20 righe contengono 900 byte
'invio 900 byte alla volta

  
  If EOF(1) Then
    tasto_update.Caption = "ERR.FILE"
    GoTo err_download
  End If
  
  On Error GoTo err_download
  
  flash = 0
  
loop_write_flash:
  
  If timer_programmazione > 500 Then GoTo err_download
  
  punta_riga = 0
  tentativi = 0
  
'If flash = 31232 Then
'  flash = 31232
'End If
  
loop_carica_righe:
  
  'carico 20 righe e il checksum
  Line Input #1, righe(punta_riga)
  If EOF(1) Then
    If righe(punta_riga) = "end file" Then
      GoTo ultime_righe
    Else
      GoTo err_download
    End If
  Else
    If punta_riga < righe_uu Then
      punta_riga = punta_riga + 1
      GoTo loop_carica_righe
    End If
  End If
  

trasmetti_in_ram:
  
  'scrivo in ram 256 byte
  cmd = "W " + Trim(Str((ram_adr_device))) + " 256"
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_write_flash
  
  'invio i dati
trasmetti_righe:
  For punta_riga = 0 To righe_uu
trasmetti_riga_n:
    invia_comando (righe(punta_riga) + vbCr + vbLf)
    attendi_risposta (righe(punta_riga) + vbCr + vbLf)
    If errore_comando = True Then
      If tentativi < 10 Then
        tentativi = tentativi + 1
        errore_comando = False
        GoTo trasmetti_riga_n
      End If
    End If
  Next
  punta_riga = punta_riga - 1
  attendi_risposta (righe(punta_riga) + vbCr + vbLf + "OK" + vbCr + vbLf)
    If errore_comando = True Then
    If tentativi < 10 Then
      tentativi = tentativi + 1
      GoTo trasmetti_righe
    Else
      GoTo err_write_flash
    End If
  End If
  
  'preparo la flash
  cmd = "P 0 " + Trim(Str(settori_device))
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_write_flash
  
  
  'copio la ram in flash
  cmd = "C " + Trim(Str(flash)) + " " + Trim(Str(ram_adr_device)) + " 256"
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_write_flash
  
  flash = flash + dim_pacchetto
  
Dim percentuale As Long
  percentuale = flash
  percentuale = percentuale * 100
  percentuale = percentuale / dimensione_file
  percentuale = Int(percentuale)
  tasto_update.Caption = Str(Trim(percentuale)) + "%"
  
  GoTo loop_write_flash
    
 
ultime_righe:

  Close #1
  GoTo fine_write_flash
  
err_download:
  text_report.Text = text_report.Text + "ERROR: can't write device!"
  errore_download = True
  tasto_update.Caption = "ERR.WRITE"
  Close #1
  
err_write_flash:
  
  text_report.Text = text_report.Text + "ERROR: can't write device!"
  errore_download = True
  tasto_update.Caption = "ERR.WRITE"
  

fine_write_flash:

  'ripristino la velocità della seriale
  uart.Settings = "19200,n,8,1"

End Sub







Private Sub scarica_programma_bin()

  Dim riga, riga_tx As String
  Dim tentativi As Integer
  Dim chk As Long

  Dim flash As Long

  On Error GoTo err_write_flash

  'è tutto pronto, devo solo inviare le righe

  'cambio frequenza per andare + veloce
  cmd = "B 38400 1"
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_write_flash

  uart.Settings = "38400,n,8,1"

  
  
inizio_download_file:
  
  Open path_file_hex + "file_codice_con_vuc.txt" For Input As #1
 
  text_report.Text = text_report.Text + "Download new version..." + vbLf
  
  
'per scrivere devo trasferire le righe in ram partendo dall'indirizzo giusto
'scrivo 256 byte alla volta
  
'le righe sono tutte pronte per la trasmissione
'ogni riga contiene 16 byte
'16 righe contengono 256 byte
'invio 256 byte alla volta

  
  If EOF(1) Then
    tasto_update.Caption = "ERR.FILE"
    GoTo err_download
  End If
  
  On Error GoTo err_download
  
  flash = 0
  chk = 0
  
  'metto echo off
  cmd = "A 0"
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)
  
loop_write_flash:
  
  If timer_programmazione > 500 Then GoTo err_download
  
  tentativi = 0
  
  riga_tx = ""
  
  'carico 16 righe
loop_carica_righe:
  Line Input #1, riga
  If EOF(1) Then
    GoTo ultime_righe
  Else
    riga_tx = riga_tx + riga
    If Len(riga_tx) < 256 * 2 Then
      GoTo loop_carica_righe
    End If
  End If
  
  'converto in binario
  riga = ""
Dim nn As Integer
  
  For nn = 0 To (Len(riga_tx) / 2) - 1
    riga = riga + Chr(dec(Mid(riga_tx, 1 + nn * 2, 2)))
  Next
  

trasmetti_in_ram:
  
  'scrivo in ram 256 byte
  cmd = "W " + Trim(Str((ram_adr_device))) + " 256"
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta ("0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_write_flash
  
  'invio i dati
trasmetti_riga:
  invia_comando (riga)
  
  'preparo la flash
  cmd = "P 0 " + Trim(Str(settori_device))
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta ("0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_write_flash
  
  
  'copio la ram in flash
  cmd = "C " + Trim(Str(flash)) + " " + Trim(Str(ram_adr_device)) + " 256"
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta ("0" + vbCr + vbLf)
  If errore_comando = True Then GoTo err_write_flash
  
  flash = flash + dim_pacchetto
  
Dim percentuale As Long
  percentuale = flash
  percentuale = percentuale * 100
  percentuale = percentuale / dimensione_file
  percentuale = Int(percentuale)
  tasto_update.Caption = Str(Trim(percentuale)) + "%"
  
  GoTo loop_write_flash
    
 
ultime_righe:

  'metto echo on
  cmd = "A 1"
  invia_comando (cmd + vbCr + vbLf)
  attendi_risposta (cmd + vbCr + vbLf + "0" + vbCr + vbLf)

  Close #1
  GoTo fine_write_flash
  
err_download:
  text_report.Text = text_report.Text + "ERROR: can't write device!"
  errore_download = True
  tasto_update.Caption = "ERR.WRITE"
  Close #1
  
err_write_flash:
  
  text_report.Text = text_report.Text + "ERROR: can't write device!"
  errore_download = True
  tasto_update.Caption = "ERR.WRITE"
  

fine_write_flash:

  'ripristino la velocità della seriale
  uart.Settings = "19200,n,8,1"

End Sub

























'converte una stringa esadecimale in un numer decimale
Private Function dec(numero_hex As String) As Double
  
  Dim numero_dec As Double
  Dim len_numero As Integer
  
  numero_dec = 0
  For len_numero = 1 To Len(numero_hex)
    numero_dec = numero_dec * 16
  
    If Mid(numero_hex, len_numero, 1) = "0" Then
      numero_dec = numero_dec + 0
    ElseIf Mid(numero_hex, len_numero, 1) = "1" Then
      numero_dec = numero_dec + 1
    ElseIf Mid(numero_hex, len_numero, 1) = "2" Then
      numero_dec = numero_dec + 2
    ElseIf Mid(numero_hex, len_numero, 1) = "3" Then
      numero_dec = numero_dec + 3
    ElseIf Mid(numero_hex, len_numero, 1) = "4" Then
      numero_dec = numero_dec + 4
    ElseIf Mid(numero_hex, len_numero, 1) = "5" Then
      numero_dec = numero_dec + 5
    ElseIf Mid(numero_hex, len_numero, 1) = "6" Then
      numero_dec = numero_dec + 6
    ElseIf Mid(numero_hex, len_numero, 1) = "7" Then
      numero_dec = numero_dec + 7
    ElseIf Mid(numero_hex, len_numero, 1) = "8" Then
      numero_dec = numero_dec + 8
    ElseIf Mid(numero_hex, len_numero, 1) = "9" Then
      numero_dec = numero_dec + 9
    ElseIf Mid(numero_hex, len_numero, 1) = "A" Then
      numero_dec = numero_dec + 10
    ElseIf Mid(numero_hex, len_numero, 1) = "B" Then
      numero_dec = numero_dec + 11
    ElseIf Mid(numero_hex, len_numero, 1) = "C" Then
      numero_dec = numero_dec + 12
    ElseIf Mid(numero_hex, len_numero, 1) = "D" Then
      numero_dec = numero_dec + 13
    ElseIf Mid(numero_hex, len_numero, 1) = "E" Then
      numero_dec = numero_dec + 14
    ElseIf Mid(numero_hex, len_numero, 1) = "F" Then
      numero_dec = numero_dec + 15
    End If
  Next
  
  dec = numero_dec
  
End Function

'converte un numero decimale in una stringa
Private Function hex(ByVal numero_dec As Double) As String
  
  Dim numero_hex As String
  Dim cifra_hex As Integer
  
  numero_hex = ""
  While numero_dec
    cifra_hex = (numero_dec - Int(numero_dec / 16) * 16)
    If cifra_hex = 0 Then
      numero_hex = "0" + numero_hex
    ElseIf cifra_hex = 1 Then
      numero_hex = "1" + numero_hex
    ElseIf cifra_hex = 2 Then
      numero_hex = "2" + numero_hex
    ElseIf cifra_hex = 3 Then
      numero_hex = "3" + numero_hex
    ElseIf cifra_hex = 4 Then
      numero_hex = "4" + numero_hex
    ElseIf cifra_hex = 5 Then
      numero_hex = "5" + numero_hex
    ElseIf cifra_hex = 6 Then
      numero_hex = "6" + numero_hex
    ElseIf cifra_hex = 7 Then
      numero_hex = "7" + numero_hex
    ElseIf cifra_hex = 8 Then
      numero_hex = "8" + numero_hex
    ElseIf cifra_hex = 9 Then
      numero_hex = "9" + numero_hex
    ElseIf cifra_hex = 10 Then
      numero_hex = "A" + numero_hex
    ElseIf cifra_hex = 11 Then
      numero_hex = "B" + numero_hex
    ElseIf cifra_hex = 12 Then
      numero_hex = "C" + numero_hex
    ElseIf cifra_hex = 13 Then
      numero_hex = "D" + numero_hex
    ElseIf cifra_hex = 14 Then
      numero_hex = "E" + numero_hex
    ElseIf cifra_hex = 15 Then
      numero_hex = "F" + numero_hex
    End If
      
    numero_dec = Int(numero_dec / 16)
  Wend
  
  If numero_hex = "" Then numero_hex = "0"
  
  hex = numero_hex
  
End Function
'converte un numero decimale in una stringa
Private Function hex_ff(ByVal numero_dec As Double) As String
  
  Dim numero_hex As String
  Dim cifra_hex As Integer
  
  numero_hex = ""
  While numero_dec
    cifra_hex = (numero_dec - Int(numero_dec / 16) * 16)
    If cifra_hex = 0 Then
      numero_hex = "0" + numero_hex
    ElseIf cifra_hex = 1 Then
      numero_hex = "1" + numero_hex
    ElseIf cifra_hex = 2 Then
      numero_hex = "2" + numero_hex
    ElseIf cifra_hex = 3 Then
      numero_hex = "3" + numero_hex
    ElseIf cifra_hex = 4 Then
      numero_hex = "4" + numero_hex
    ElseIf cifra_hex = 5 Then
      numero_hex = "5" + numero_hex
    ElseIf cifra_hex = 6 Then
      numero_hex = "6" + numero_hex
    ElseIf cifra_hex = 7 Then
      numero_hex = "7" + numero_hex
    ElseIf cifra_hex = 8 Then
      numero_hex = "8" + numero_hex
    ElseIf cifra_hex = 9 Then
      numero_hex = "9" + numero_hex
    ElseIf cifra_hex = 10 Then
      numero_hex = "A" + numero_hex
    ElseIf cifra_hex = 11 Then
      numero_hex = "B" + numero_hex
    ElseIf cifra_hex = 12 Then
      numero_hex = "C" + numero_hex
    ElseIf cifra_hex = 13 Then
      numero_hex = "D" + numero_hex
    ElseIf cifra_hex = 14 Then
      numero_hex = "E" + numero_hex
    ElseIf cifra_hex = 15 Then
      numero_hex = "F" + numero_hex
    End If
      
    numero_dec = Int(numero_dec / 16)
  Wend
  
  If numero_hex = "" Then numero_hex = "0"
  If Len(numero_hex) < 2 Then numero_hex = "0" + numero_hex
  
  hex_ff = numero_hex
  
End Function





Private Sub invia_comando(comando As String)
  Dim tx As String
  
  rx_cmd = ""
  tx_cmd = comando
  uart.Output = tx_cmd
  End Sub


Private Sub attendi_risposta(stringa As String)
  Dim xx, bb As Integer
  
  On Error GoTo errore_attesa_risposta
  
bb = 1
  'devo epurare le stringhe dei carattere CR e LF
  xx = 1
  While xx <= Len(stringa)
    If Asc(Mid(stringa, xx, 1)) = 13 Then
      stringa = Left(stringa, xx - 1) + Right(stringa, Len(stringa) - xx)
    ElseIf Asc(Mid(stringa, xx, 1)) = 10 Then
      stringa = Left(stringa, xx - 1) + Right(stringa, Len(stringa) - xx)
    Else
      xx = xx + 1
    End If
  Wend
bb = 2
  centesimi = 0
  While centesimi < 300
    DoEvents
    aaa = uart.Input
bb = 20
    If Len(aaa) > 0 Then
      'devo epurare le stringhe dei carattere CR e LF
bb = 21
      xx = 1
      While xx <= Len(aaa)
bb = 22
        If Asc(Mid(aaa, xx, 1)) = 13 Then
          aaa = Left(aaa, xx - 1) + Right(aaa, Len(aaa) - xx)
        ElseIf Asc(Mid(aaa, xx, 1)) = 10 Then
          aaa = Left(aaa, xx - 1) + Right(aaa, Len(aaa) - xx)
        Else
          xx = xx + 1
        End If
      Wend
bb = 23
      rx_cmd = rx_cmd + aaa
      If Len(rx_cmd) >= Len(stringa) Then centesimi = 1000
bb = 24
    End If
  Wend
bb = 3
 If Mid(rx_cmd, 1, Len(rx_cmd)) = Mid(stringa, 1, Len(rx_cmd)) Then
    errore_comando = False
 Else
  'trovo il carattere di differenza,
  If Len(rx_cmd) > Len(stringa) Then
    errore_comando = True
  Else
    For xx = 1 To Len(rx_cmd)
      If Mid(rx_cmd, xx, 1) <> Mid(stringa, xx, 1) Then
        errore_comando = True
        xx = 1000
      End If
    Next
  End If
 End If
bb = 4
 GoTo fine_attesa_risposta

errore_attesa_risposta:
  errore_comando = True
  
fine_attesa_risposta:
  
End Sub



Private Sub nop()

End Sub
