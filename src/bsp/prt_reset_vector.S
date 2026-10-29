.equ DAIF_MASK, 0x1C0
.global OsVectorTable
.global OsEnterMain
.section .text.startup, "ax"
OsEnterMain:
    BL main
    MOV x2, DAIF_MASK
    MSR DAIF, x2
EXITLOOP:
    B EXITLOOP
