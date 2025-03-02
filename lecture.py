lecture_description = [
    """
RAXレジスタに0x12345を代入してください
""",
    """
RAXレジスタに0x12345を代入します
次に、RAXレジスタの値をRDXレジスタにコピーします
最後に、RBXレジスタの値を0x54321にしてください
""",
    """
RAXレジスタに0x12345を代入し、次にRDXレジスタに0x54321を代入してください
その後、RBXレジスタにRAXレジスタとRDXレジスタの値を足した値を代入してください
次に、RCXレジスタにRDXレジスタからRAXレジスタの値を引いた値を代入してください
最後に、RAXレジスタにRAXレジスタとRCXレジスタの値をXORした値を代入してください
""",
    """
RAXレジスタに0x12345を代入し、次にRDXレジスタに好きな値を代入してください
その後、RAXレジスタの値とRDXレジスタの値が等しい場合はRDXレジスタの値を0x100に、
等しくない場合はRDXレジスタの値を0x200にしてください
""",
    """
RAXレジスタに0x12345を代入し、RAXレジスタの値をスタックにプッシュしてください
""",
    """
RAXレジスタに0x12345を代入し、RAXレジスタの値を何度もスタックにプッシュしながら、1回ポップしRBXレジスタに代入してください
""",
    """
標準出力のシステムコールを使って、スタックにプッシュした文字列「Hello!」を出力してください
""",
    """
flag.txtファイルを読み込み、その内容を標準出力に出力してください
""",
    """
引数の値(0x5)を2倍にして返り値を返す関数を実装してください
""",
    """
以下のアセンブリコードを読み解いて、求められる入力値を見つけてください
""",
]

lecture_answer = [
    """
mov  rax, 0x12345
""",
    """
mov  rax, 0x12345
mov  rdx, rax
mov  rbx, 0x54321
""",
    """
mov  rax, 0x12345
mov  rdx, 0x54321
mov  rbx, rax
add  rbx, rdx
mov  rcx, rdx
sub  rcx, rax
xor  rax, rcx
""",
    """
mov  rax, 0x12345
mov  rdx, 0xabcde
cmp  rax, rdx
jne  not_equal
mov  rdx, 0x100
jmp  done
not_equal:
mov  rdx, 0x200
done:
""",
    """
mov  rax, 0x12345
push rax
""",
    """
mov  rax, 0x12345
push rax
push rax
pop  rbx
""",
    """
mov  rax, 0x216f6c6c6548
push rax
mov  rax, 1
mov  rdi, 1
mov  rsi, rsp
mov  rdx, 0x6
syscall
""",
    """
mov  rax, 0                  # null terminate
push rax                     # push null to stack
mov  rax, 0x7478742e67616c66 # "flag.txt"
push rax                     # push file name to stack

mov  rdi, rsp  # file name buffer pointer
mov  rsi, 0    # O_RDONLY
mov  rax, 2    # syscall number

syscall        # sys_open

mov  rdi, rax  # fd
mov  rsi, rsp  # buffer pointer
mov  rdx, 1024 # buffer size
mov  rax, 0    # syscall number

syscall        # sys_read

mov  rdx, rax  # buffer size
mov  rsi, rsp  # buffer pointer
mov  rdi, 1    # stdout
mov  rax, 1    # syscall number

syscall        # sys_write
""",
]
