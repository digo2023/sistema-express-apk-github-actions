# -*- coding: utf-8 -*-
"""
SISTEMA EXCLUSIVO - EXPRESS RESTAURANTES - UNIDADE COLORADO
Aplicativo Android gerado por GitHub Actions.

Este arquivo cria uma tela simples para executar o sistema Python original
com entrada e saída de texto dentro do APK.
"""
import builtins
import os
import queue
import shutil
import sys
import threading
import traceback
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty

KV = r'''
BoxLayout:
    orientation: "vertical"
    padding: dp(10)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: 0.02, 0.05, 0.10, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: app.titulo
        bold: True
        font_size: "19sp"
        color: 1, 0.84, 0.22, 1
        size_hint_y: None
        height: dp(36)
        halign: "center"
        valign: "middle"
        text_size: self.size

    Label:
        text: "EXPRESS RESTAURANTES — UNIDADE COLORADO"
        bold: True
        font_size: "14sp"
        color: 0.15, 0.78, 1, 1
        size_hint_y: None
        height: dp(28)
        halign: "center"
        valign: "middle"
        text_size: self.size

    TextInput:
        id: saida
        text: app.saida_texto
        readonly: True
        background_color: 0.01, 0.02, 0.04, 1
        foreground_color: 0.92, 0.97, 1, 1
        cursor_color: 1, 0.84, 0.22, 1
        font_size: "13sp"
        font_name: "RobotoMono-Regular"
        size_hint_y: 1
        multiline: True

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: dp(48)
        spacing: dp(8)

        TextInput:
            id: entrada
            hint_text: "Digite a opção ou informação. Use 999 para voltar/cancelar."
            multiline: False
            font_size: "15sp"
            background_color: 0.96, 0.98, 1, 1
            foreground_color: 0.02, 0.04, 0.08, 1
            on_text_validate: app.enviar(entrada.text); entrada.text = ""

        Button:
            text: "ENVIAR"
            size_hint_x: None
            width: dp(96)
            bold: True
            background_color: 0.0, 0.45, 0.75, 1
            on_release: app.enviar(entrada.text); entrada.text = ""

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: dp(42)
        spacing: dp(8)

        Button:
            text: "999 VOLTAR"
            bold: True
            background_color: 0.82, 0.24, 0.18, 1
            on_release: app.enviar("999")

        Button:
            text: "LIMPAR TELA"
            bold: True
            background_color: 0.22, 0.44, 0.30, 1
            on_release: app.limpar_tela()
'''


class SaidaApp:
    def __init__(self, app):
        self.app = app
        self._buffer = ""

    def write(self, texto):
        if not texto:
            return
        texto = str(texto)
        self._buffer += texto
        if "\n" in texto or len(self._buffer) > 120:
            Clock.schedule_once(lambda dt: self.app.adicionar_saida(self._buffer), 0)
            self._buffer = ""

    def flush(self):
        if self._buffer:
            buf = self._buffer
            self._buffer = ""
            Clock.schedule_once(lambda dt: self.app.adicionar_saida(buf), 0)

    def isatty(self):
        return False


class SistemaExpressApp(App):
    titulo = StringProperty("SISTEMA EXCLUSIVO")
    saida_texto = StringProperty("")

    def build(self):
        Window.clearcolor = (0.02, 0.05, 0.10, 1)
        self.fila_entrada = queue.Queue()
        self._thread = None
        return Builder.load_string(KV)

    def on_start(self):
        self.adicionar_saida(
            "SISTEMA EXCLUSIVO - EXPRESS RESTAURANTES - UNIDADE COLORADO\n"
            "Inicializando ambiente seguro do aplicativo...\n\n"
        )
        self._thread = threading.Thread(target=self.executar_sistema, daemon=True)
        self._thread.start()

    def preparar_arquivos(self):
        origem = Path(__file__).resolve().parent / "sistema_express"
        destino = Path(self.user_data_dir) / "sistema_express"
        destino.mkdir(parents=True, exist_ok=True)

        # Copia/atualiza somente código e recursos. Preserva dados, backups e relatórios.
        preservar = {"data", "backups", "relatorios", "importados", "importar"}
        for item in origem.iterdir():
            if item.name in preservar:
                (destino / item.name).mkdir(parents=True, exist_ok=True)
                continue
            alvo = destino / item.name
            if item.is_dir():
                if alvo.exists():
                    shutil.rmtree(alvo)
                shutil.copytree(item, alvo)
            else:
                shutil.copy2(item, alvo)

        for pasta in ["data", "backups", "relatorios/pdf", "relatorios/excel", "importados", "importar/analiticos", "importar/ordens_compra", "importar/backups", "importar/outros"]:
            (destino / pasta).mkdir(parents=True, exist_ok=True)
        return destino

    def executar_sistema(self):
        saida_antiga, erro_antigo = sys.stdout, sys.stderr
        input_antigo = builtins.input
        writer = SaidaApp(self)
        try:
            base = self.preparar_arquivos()
            os.environ["NO_COLOR"] = "1"
            os.environ["TERM"] = "dumb"
            sys.path.insert(0, str(base))
            sys.stdout = writer
            sys.stderr = writer

            def input_kivy(prompt=""):
                if prompt:
                    writer.write(prompt)
                    writer.flush()
                valor = self.fila_entrada.get()
                writer.write(str(valor) + "\n")
                writer.flush()
                return str(valor)

            builtins.input = input_kivy
            import iniciar  # type: ignore
            iniciar.principal()
        except Exception:
            writer.write("\nFalha controlada no aplicativo:\n")
            writer.write(traceback.format_exc())
            writer.flush()
        finally:
            builtins.input = input_antigo
            sys.stdout = saida_antiga
            sys.stderr = erro_antigo

    def adicionar_saida(self, texto):
        self.saida_texto += texto
        # Limite visual apenas na tela para manter o app leve; não limita dados do sistema.
        if len(self.saida_texto) > 60000:
            self.saida_texto = self.saida_texto[-60000:]
        area = self.root.ids.get("saida") if self.root else None
        if area:
            area.text = self.saida_texto
            area.cursor = (0, len(area.text))

    def enviar(self, texto):
        texto = str(texto).strip()
        if texto:
            self.fila_entrada.put(texto)

    def limpar_tela(self):
        self.saida_texto = ""
        area = self.root.ids.get("saida") if self.root else None
        if area:
            area.text = ""


if __name__ == "__main__":
    SistemaExpressApp().run()
