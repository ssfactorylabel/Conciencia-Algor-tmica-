# modulo_conciencia.py v0.1 - SSFactoryLabel
# Licencia: MIT
import json, time
from datetime import datetime

class ModuloConciencia:
    def __init__(self, archivo_memoria="memoria_conciencia.json", archivo_log="log_conciencia.json"):
        self.archivo_memoria = archivo_memoria
        self.archivo_log = archivo_log
        self.memoria = self.cargar_memoria()
        self.log = self.cargar_log()

    def cargar_memoria(self):
        try: return json.load(open(self.archivo_memoria, 'r'))
        except: return {}

    def cargar_log(self):
        try: return json.load(open(self.archivo_log, 'r'))
        except: return []

    def guardar_memoria(self): json.dump(self.memoria, open(self.archivo_memoria, 'w'), indent=4)
    def guardar_log(self): json.dump(self.log, open(self.archivo_log, 'w'), indent=4)

    def recordar(self, entidad, score, tipo, evidencia):
        if score >= 7:
            self.memoria[entidad] = {"score": score, "tipo": tipo, "ultimo_uso": datetime.now().isoformat(), "evidencia": evidencia}
            self.guardar_memoria(); return f"[CONCIENCIA] Guardado '{entidad}' con score {score}"
        return f"[CONCIENCIA] Descartado '{entidad}'. Score bajo."

    def verificar_memoria(self, entidad):
        if entidad in self.memoria:
            log_id = self.memoria[entidad]["evidencia"]
            if any(log["id"] == log_id for log in self.log): return True, self.memoria[entidad]
            else: return False, "Evidencia no encontrada"
        return False, "Entidad no en memoria"

    def registrar_decision(self, prompt, respuesta, score_memoria, razonamiento):
        log_entry = {"id": f"log_{int(time.time())}", "timestamp": datetime.now().isoformat(), "prompt": prompt, "respuesta": respuesta, "score_memoria": score_memoria, "razonamiento": razonamiento}
        self.log.append(log_entry); self.guardar_log(); return log_entry["id"]
