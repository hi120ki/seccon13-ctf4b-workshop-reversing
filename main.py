import os
import shutil
import uuid

import timeout_decorator
from ctf import assembly, ctf_answer, ctf_description
from flask import Flask, redirect, render_template, request
from lecture import lecture_answer, lecture_description
from pwn import asm
from qiling import Qiling
from qiling.const import QL_ARCH, QL_OS, QL_VERBOSE
from qiling.extensions import pipe

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/lecture/<int:id>", methods=["GET"])
def lecture(id):
    if id < 1 or id > 8:
        return redirect("/")

    return render_template(
        "challenge.html",
        mode="lecture",
        id=id,
        description=lecture_description[id - 1],
        answer=lecture_answer[id - 1],
        rax=hex(0x0),
        rbx=hex(0x0),
        rcx=hex(0x0),
        rdx=hex(0x0),
        rsi=hex(0x0),
        rdi=hex(0x0),
        rbp=hex(0x0),
        rip=hex(0x0),
        rsp=hex(0x0),
        stack=[],
    )


@app.route("/ctf/<int:id>", methods=["GET"])
def ctf(id):
    if id < 1 or id > 3:
        return redirect("/")

    if id == 3:
        return render_template(
            "asm.html",
            mode="ctf",
            id=id,
            asm=assembly,
            description=ctf_description[id - 1],
            answer=ctf_answer[id - 1],
        )

    return render_template(
        "challenge.html",
        mode="ctf",
        id=id,
        description=ctf_description[id - 1],
        answer=ctf_answer[id - 1],
        rax=hex(0x0),
        rbx=hex(0x0),
        rcx=hex(0x0),
        rdx=hex(0x0),
        rsi=hex(0x0),
        rdi=hex(0x0),
        rbp=hex(0x0),
        rip=hex(0x0),
        rsp=hex(0x0),
        stack=[],
    )


def lecture_error(id, error):
    return render_template(
        "challenge.html",
        mode="lecture",
        id=id,
        description=lecture_description[id - 1],
        answer=lecture_answer[id - 1],
        error=error,
        stack=[],
    )


def ctf_error(id, error):
    return render_template(
        "challenge.html",
        mode="ctf",
        id=id,
        description=ctf_description[id - 1],
        answer=ctf_answer[id - 1],
        error=error,
        stack=[],
    )


def get_stack(ql):
    stack = []
    rsp = ql.arch.regs.read("rsp")
    for i in range(9):
        addr = rsp + i * 8 - 8
        stack.append(f"{hex(addr)} (rsp+{i * 8}) {hex(ql.mem.read_ptr(addr))}")
    return stack


@app.route("/lecture/<int:id>", methods=["POST"])
def lecture_post(id):
    if id < 1 or id > 10:
        return redirect("/")

    # 入力されたアセンブリコードを取得
    code = request.form["code"]

    if id == 10:
        if code.strip() == "ctf4b{awes0me!}":
            return render_template(
                "asm.html",
                mode="lecture",
                id=id,
                asm=assembly[0],
                message="おめでとうございます！正解です！",
                description=lecture_description[id - 1],
                answer=lecture_answer[id - 1],
            )
        else:
            return render_template(
                "asm.html",
                mode="lecture",
                id=id,
                asm=assembly[0],
                message="入力された文字列はフラグと一致しませんでした",
                description=lecture_description[id - 1],
                answer=lecture_answer[id - 1],
            )

    # アセンブリコードの検証
    if len(code.strip()) == 0:
        return lecture_error(id, "アセンブリコードを入力してください")
    if ";" in code:
        return lecture_error(id, "セミコロンは使えません")
    lines = code.splitlines()
    if len(lines) > 50:
        return lecture_error(id, "50行以内で入力してください")

    try:
        return lecture_exec(id, code)
    except Exception as e:
        return lecture_error(id, str(e))


@timeout_decorator.timeout(3, use_signals=False)
def lecture_exec(id, code):
    # アセンブリコードをアセンブル
    try:
        asm_code = asm(code, arch="amd64", os="linux")
    except Exception as e:
        return lecture_error(
            id, "アセンブリコードのアセンブルに失敗しました : " + str(e)
        )

    # ディレクトリを作成
    dirname = str(uuid.uuid4())
    os.mkdir(dirname)
    if id == 8:
        f = open(os.path.join(dirname, "flag.txt"), "w")
        flag = "ctf4b{gre4t_y0u_g0t_1t}"
        f.write(flag)
        f.close()

    # Qilingで実行
    try:
        ql = Qiling(
            code=asm_code,
            rootfs=dirname,
            archtype=QL_ARCH.X8664,
            ostype=QL_OS.LINUX,
            verbose=QL_VERBOSE.DEFAULT,
        )
        ql.os.stdout = pipe.SimpleOutStream(0)
    except Exception as e:
        return lecture_error(id, "仮想環境の初期化に失敗しました : " + str(e))

    try:
        ql.run()
    except Exception as e:
        return lecture_error(id, "コードの実行に失敗しました : " + str(e))

    try:
        stdout = ql.os.stdout.read(1024).decode().strip()
    except Exception:
        stdout = str(ql.os.stdout.read(1024))

    # 実行後レジスタの値を取得
    rax = ql.arch.regs.read("rax")
    rbx = ql.arch.regs.read("rbx")
    rcx = ql.arch.regs.read("rcx")
    rdx = ql.arch.regs.read("rdx")
    rsi = ql.arch.regs.read("rsi")
    rdi = ql.arch.regs.read("rdi")
    rbp = ql.arch.regs.read("rbp")
    rip = ql.arch.regs.read("rip")
    rsp = ql.arch.regs.read("rsp")

    # 正解判定
    message = "正しく実行されました"
    if id == 1 and rax == 0x12345:
        message = "おめでとうございます！正解です！"
    if id == 2 and rax == 0x12345 and rdx == 0x12345 and rbx == 0x54321:
        message = "おめでとうございます！正解です！"
    if (
        id == 3
        and rax == 0x53C99
        and rbx == 0x66666
        and rcx == 0x41FDC
        and rdx == 0x54321
    ):
        message = "おめでとうございます！正解です！"
    if id == 4 and (rdx == 0x100 or rdx == 0x200):
        message = "おめでとうございます！正解です！"
    if id == 5 and ql.arch.stack_pop() == 0x12345:
        message = "おめでとうございます！正解です！"
    if id == 6 and ql.arch.stack_pop() == 0x12345 and rbx == 0x12345:
        message = "おめでとうございます！正解です！"
    if id == 7 and "Hello!" in stdout:
        message = "おめでとうございます！正解です！"
    if id == 8 and "ctf4b{gre4t_y0u_g0t_1t}" in stdout:
        message = "おめでとうございます！正解です！"

    shutil.rmtree(dirname, ignore_errors=True)

    return render_template(
        "challenge.html",
        mode="lecture",
        id=id,
        description=lecture_description[id - 1],
        answer=lecture_answer[id - 1],
        message=message,
        stdout=stdout,
        rax=hex(rax),
        rbx=hex(rbx),
        rcx=hex(rcx),
        rdx=hex(rdx),
        rsi=hex(rsi),
        rdi=hex(rdi),
        rbp=hex(rbp),
        rip=hex(rip),
        rsp=hex(rsp),
        stack=get_stack(ql),
    )


@app.route("/ctf/<int:id>", methods=["POST"])
def ctf_post(id):
    if id < 1 or id > 3:
        return redirect("/")

    code = request.form["code"]

    if id == 3:
        message = ""
        if code.strip() == "ctf4b{th4nk_y0u!}":
            message = ("おめでとうございます！正解です！",)
        else:
            message = ("入力された文字列はフラグと一致しませんでした",)
        return render_template(
            "asm.html",
            mode="lecture",
            id=id,
            asm=assembly,
            message=message,
            description=lecture_description[id - 1],
            answer=lecture_answer[id - 1],
        )

    # アセンブリコードの検証
    if len(code.strip()) == 0:
        return ctf_error(id, "アセンブリコードを入力してください")
    if ";" in code:
        return ctf_error(id, "セミコロンは使えません")
    lines = code.splitlines()
    if len(lines) > 50:
        return ctf_error(id, "50行以内で入力してください")

    try:
        return ctf_exec(id, code)
    except Exception as e:
        return ctf_error(id, str(e))


@timeout_decorator.timeout(3, use_signals=False)
def ctf_exec(id, code):
    # アセンブリコードをアセンブル
    try:
        asm_code = asm(code, arch="amd64", os="linux")
    except Exception as e:
        return ctf_error(id, "アセンブリコードのアセンブルに失敗しました : " + str(e))

    # ディレクトリを作成
    dirname = str(uuid.uuid4())
    os.mkdir(dirname)

    # Qilingで実行
    try:
        ql = Qiling(
            code=asm_code,
            rootfs=dirname,
            archtype=QL_ARCH.X8664,
            ostype=QL_OS.LINUX,
            verbose=QL_VERBOSE.DEFAULT,
        )
        ql.os.stdout = pipe.SimpleOutStream(0)
    except Exception as e:
        return lecture_error(id, "仮想環境の初期化に失敗しました : " + str(e))

    try:
        ql.run()
    except Exception as e:
        return ctf_error(id, "コードの実行に失敗しました : " + str(e))

    try:
        stdout = ql.os.stdout.read(1024).decode().strip()
    except Exception:
        stdout = str(ql.os.stdout.read(1024))

    # 実行後レジスタの値を取得
    rax = ql.arch.regs.read("rax")
    rbx = ql.arch.regs.read("rbx")
    rcx = ql.arch.regs.read("rcx")
    rdx = ql.arch.regs.read("rdx")
    rsi = ql.arch.regs.read("rsi")
    rdi = ql.arch.regs.read("rdi")
    rbp = ql.arch.regs.read("rbp")
    rip = ql.arch.regs.read("rip")
    rsp = ql.arch.regs.read("rsp")

    # 正解判定
    message = "正しく実行されました"
    if id == 1 and rax == 0x0 and rbx == 0x66666 and rcx == 0x41FDC and rdx == 0xFFFFF:
        message = "おめでとうございます！正解です！"
    if id == 2:
        try:
            f = open(os.path.join(dirname, "flag.txt"), "rb")
            hex_data = f.read().hex()
            f.close()
        except Exception:
            hex_data = ""
        try:
            f = open(os.path.join(dirname, "flag.txt"))
            flag = f.read().strip()
            f.close()
            if flag == "ctf4b{we1come_t0_the_SECCON_13_Beg1nner3_W0rksh0p}":
                message = "おめでとうございます！正解です！ : " + flag
            else:
                message = "flag.txtの内容が正しくありません : " + flag
        except Exception as e:
            message = "flag.txtの読み込みに失敗しました : " + hex_data + " " + str(e)

    shutil.rmtree(dirname, ignore_errors=True)

    return render_template(
        "challenge.html",
        mode="ctf",
        id=id,
        description=ctf_description[id - 1],
        answer=ctf_answer[id - 1],
        message=message,
        stdout=stdout,
        rax=hex(rax),
        rbx=hex(rbx),
        rcx=hex(rcx),
        rdx=hex(rdx),
        rsi=hex(rsi),
        rdi=hex(rdi),
        rbp=hex(rbp),
        rip=hex(rip),
        rsp=hex(rsp),
        stack=get_stack(ql),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
