ctf_description = [
    """
RAX に 0x12345 を代入し、RDX に 0x54321 を代入してください。
RBX に RAX と RDX の和を代入してください。
RCX に RDX から RAX を引いた値を代入してください。
RAX に RAX と RAX の XOR を取った結果を代入してください。
RDX に RBX と RCX の AND を取った結果を代入してください。
RAX が 0 なら、RDX に 0xFFFFF を代入してください。
RAX が 0 でないなら、RDX に 0xBEEF を代入してください。
""",
    """
flag.txtファイルに「ctf4b{we1come_t0_the_SECCON_13_Beg1nner3_W0rksh0p}」を書き込んでください
""",
    """
以下のアセンブリコードを読み解いて、求められる入力値を見つけてください
""",
]

ctf_answer = [
    """
mov  rax, 0x12345
mov  rdx, 0x54321
mov  rbx, rax
add  rbx, rdx
mov  rcx, rdx
sub  rcx, rax
xor  rax, rax
mov  rdx, rbx
and  rdx, rcx
cmp  rax, 0
jne  not_equal
mov  rdx, 0xFFFFF
jmp  done
not_equal:
mov  rdx, 0xBEEF
done:
""",
    """
mov rax, 0x7d703068736b7230
push rax
mov rax, 0x575f3372656e6e31
push rax
mov rax, 0x6765425f33315f4e
push rax
mov rax, 0x4f434345535f6568
push rax
mov rax, 0x745f30745f656d6f
push rax
mov rax, 0x633165777b623466
push rax
mov rax, 0x7463000000000000
push rax

mov rax, 0x7478742e67616c66 # "flag.txt"
push rax                    # push file name to stack
mov rdi, rsp                # file name buffer pointer
mov rsi, 0x41               # O_WRONLY | O_CREAT
mov rdx, 0644               # permission
mov rax, 2                  # syscall number for sys_open
syscall

add rsp, 14   # remove "flag.txt" from stack
mov rdi, rax  # fd
mov rsi, rsp  # buffer pointer
mov rdx, 50   # flag length
mov rax, 1    # syscall number for sys_write
syscall

mov rdi, rax  # fd
mov rax, 3    # syscall number for sys_close
syscall

mov rax, 60   # syscall number for sys_exit
xor rdi, rdi  # status 0
syscall
""",
    """
ctf4b{th4nk_y0u!}
""",
]


assembly = """
0000000000401156 <check_char>:
    401156:  endbr64
    40115a:  push   rbp
    40115b:  mov    rbp,rsp
    40115e:  mov    eax,edi
    401160:  mov    DWORD PTR [rbp-0x18],esi
    401163:  mov    QWORD PTR [rbp-0x20],rdx
    401167:  mov    BYTE PTR [rbp-0x14],al
    40116a:  movsx  eax,BYTE PTR [rbp-0x14]
    40116e:  mov    DWORD PTR [rbp-0x4],eax
    401171:  mov    rcx,QWORD PTR [rbp-0x20]
    401175:  movabs rdx,0xaaaaaaaaaaaaaaab
    40117f:  mov    rax,rcx
    401182:  mul    rdx
    401185:  mov    rax,rdx
    401188:  shr    rax,1
    40118b:  mov    rdx,rax
    40118e:  add    rdx,rdx
    401191:  add    rdx,rax
    401194:  mov    rax,rcx
    401197:  sub    rax,rdx
    40119a:  test   rax,rax
    40119d:  jne    4011a5 <check_char+0x4f>
    40119f:  xor    DWORD PTR [rbp-0x4],0x15
    4011a3:  jmp    4011de <check_char+0x88>
    4011a5:  mov    rcx,QWORD PTR [rbp-0x20]
    4011a9:  movabs rdx,0xaaaaaaaaaaaaaaab
    4011b3:  mov    rax,rcx
    4011b6:  mul    rdx
    4011b9:  mov    rax,rdx
    4011bc:  shr    rax,1
    4011bf:  mov    rdx,rax
    4011c2:  add    rdx,rdx
    4011c5:  add    rdx,rax
    4011c8:  mov    rax,rcx
    4011cb:  sub    rax,rdx
    4011ce:  cmp    rax,0x1
    4011d2:  jne    4011da <check_char+0x84>
    4011d4:  add    DWORD PTR [rbp-0x4],0x7
    4011d8:  jmp    4011de <check_char+0x88>
    4011da:  add    DWORD PTR [rbp-0x4],0x3
    4011de:  mov    eax,DWORD PTR [rbp-0x4]
    4011e1:  cmp    eax,DWORD PTR [rbp-0x18]
    4011e4:  sete   al
    4011e7:  movzx  eax,al
    4011ea:  pop    rbp
    4011eb:  ret

00000000004011ec <main>:
    4011ec:  endbr64
    4011f0:  push   rbp
    4011f1:  mov    rbp,rsp
    4011f4:  sub    rsp,0x260
    4011fb:  mov    DWORD PTR [rbp-0x260],0x76
    401205:  mov    DWORD PTR [rbp-0x25c],0x7b
    40120f:  mov    DWORD PTR [rbp-0x258],0x69
    401219:  mov    DWORD PTR [rbp-0x254],0x21
    401223:  mov    DWORD PTR [rbp-0x250],0x69
    40122d:  mov    DWORD PTR [rbp-0x24c],0x7e
    401237:  mov    DWORD PTR [rbp-0x248],0x61
    401241:  mov    DWORD PTR [rbp-0x244],0x6f
    40124b:  mov    DWORD PTR [rbp-0x240],0x37
    401255:  mov    DWORD PTR [rbp-0x23c],0x7b
    40125f:  mov    DWORD PTR [rbp-0x238],0x72
    401269:  mov    DWORD PTR [rbp-0x234],0x62
    401273:  mov    DWORD PTR [rbp-0x230],0x6c
    40127d:  mov    DWORD PTR [rbp-0x22c],0x37
    401287:  mov    DWORD PTR [rbp-0x228],0x78
    401291:  mov    DWORD PTR [rbp-0x224],0x34
    40129b:  mov    DWORD PTR [rbp-0x220],0x84
    4012a5:  lea    rax,[rbp-0x210]
    4012ac:  mov    rsi,rax
    4012af:  lea    rax,[rip+0xd4e]        # 402004 <_IO_stdin_used+0x4>
    4012b6:  mov    rdi,rax
    4012b9:  mov    eax,0x0
    4012be:  call   401060 <__isoc99_scanf@plt>
    4012c3:  mov    QWORD PTR [rbp-0x8],0x0
    4012cb:  jmp    401318 <main+0x12c>
    4012cd:  mov    rax,QWORD PTR [rbp-0x8]
    4012d1:  mov    ecx,DWORD PTR [rbp+rax*4-0x260]
    4012d8:  lea    rdx,[rbp-0x210]
    4012df:  mov    rax,QWORD PTR [rbp-0x8]
    4012e3:  add    rax,rdx
    4012e6:  movzx  eax,BYTE PTR [rax]
    4012e9:  movsx  eax,al
    4012ec:  mov    rdx,QWORD PTR [rbp-0x8]
    4012f0:  mov    esi,ecx
    4012f2:  mov    edi,eax
    4012f4:  call   401156 <check_char>
    4012f9:  test   eax,eax
    4012fb:  jne    401313 <main+0x127>
    4012fd:  lea    rax,[rip+0xd05]        # 402009 <_IO_stdin_used+0x9>
    401304:  mov    rdi,rax
    401307:  call   401050 <puts@plt>
    40130c:  mov    eax,0x1
    401311:  jmp    401324 <main+0x138>
    401313:  add    QWORD PTR [rbp-0x8],0x1
    401318:  cmp    QWORD PTR [rbp-0x8],0x10
    40131d:  jbe    4012cd <main+0xe1>
    40131f:  mov    eax,0x0
    401324:  leave
    401325:  ret
"""
