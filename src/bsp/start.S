.global OsEnterMain
.extern __os_sys_sp_end
.section .text.bspinit, "ax"
.balign 4
.global OsElxState
OsElxState:
    MRS x6, CurrentEL
    MOV x2, #0x4
    CMP w6, w2
    BEQ Start
OsEl2Entry:
    B OsEl2Entry
Start:
    LDR x1, =__os_sys_sp_end
    BIC sp, x1, #0xf
    B OsEnterMain
OsEnterReset:
    B OsEnterReset
