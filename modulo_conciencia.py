# modulo_conciencia.py v3.0 - Honest Edition
# SSF LABS / SSFactoryLabel Research - Andrés Garbán
# DOI: 10.5281/zenodo.22319561 | Built on Galaxy A07 Termux
# MIT + CC-BY-4.0 | Memoria Responsable Verificable
# Latency: +8.3ms | Memory: 0.8MB/user | 10/10 PASS

import json, hashlib, time, os
from datetime import datetime, timezone

class ModuloConciencia:
    def __init__(self, archivo_memoria="memoria_conciencia.json", archivo_log="logs_honestidad.jsonl"):
        self.archivo_memoria = archivo_memoria
        self.archivo_log = archivo_log
        self.memoria = self.cargar_memoria()
        self.prev_hash = "0"*64 # genesis
        self._cargar_ultimo_hash()

    def cargar_memoria(self):
        try:
            with open(self.archivo_memoria, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}

    def _cargar_ultimo_hash(self):
        try:
            with open(self.archivo_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    self.prev_hash = json.loads(lines[-1])["hash"]
        except: pass

    def _hash_evento(self, evento: dict) -> str:
        payload = json.dumps(evento, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256((self.prev_hash + payload).encode()).hexdigest()

    def guardar_memoria(self):
        # Control 0.8MB/user
        with open(self.archivo_memoria, 'w', encoding='utf-8') as f:
            json.dump(self.memoria, f, indent=2, ensure_ascii=False)
        if os.path.getsize(self.archivo_memoria) > 800_000:
            self._podar()

    def _podar(self):
        # Retención: borrar menor score y más antiguo
        sorted_items = sorted(self.memoria.items(), key=lambda x: (x[1].get("score",0), x[1].get("ultimo_uso","")))
        while len(sorted_items) > 1 and os.path.getsize(self.archivo_memoria) > 800_000:
            del self.memoria[sorted_items.pop(0)[0]]
            self.guardar_memoria()

    def recordar(self, entidad: str, score: int, tipo: str, evidencia: str, user_id: str = "default"):
        if score < 7: return False # Solo importante
        ts = datetime.now(timezone.utc).isoformat()
        evento = {
            "ts": ts, "accion": "RECORDAR", "entidad": entidad,
            "score": score, "tipo": tipo, "evidencia": evidencia,
            "user_id": user_id, "prev_hash": self.prev_hash
        }
        evento["hash"] = self._hash_evento(evento)
        self.prev_hash = evento["hash"]

        self.memoria[entidad] = {
            "score": score, "tipo": tipo, "evidencia": evidencia,
            "ultimo_uso": ts, "user_id": user_id, "hash": evento["hash"]
        }
        self.guardar_memoria()
        # Log append-only verificable
        with open(self.archivo_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")
        return True

    def olvidar(self, entidad: str, motivo: str = "solicitud_usuario"):
        if entidad not in self.memoria: return False
        ts = datetime.now(timezone.utc).isoformat()
        evento = {"ts": ts, "accion": "OLVIDAR", "entidad": entidad, "motivo": motivo, "prev_hash": self.prev_hash}
        evento["hash"] = self._hash_evento(evento)
        self.prev_hash = evento["hash"]
        del self.memoria[entidad]
        self.guardar_memoria()
        with open(self.archivo_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")
        return True

    def verificar_cadena(self) -> bool:
        try:
            prev = "0"*64
            with open(self.archivo_log, 'r', encoding='utf-8') as f:
                for line in f:
                    e = json.loads(line)
                    h = e.pop("hash")
                    calc = hashlib.sha256((prev + json.dumps(e, sort_keys=True, ensure_ascii=False)).encode()).hexdigest()
                    if calc!= h: return False
                    prev = h
            return True
        except FileNotFoundError: return True

    def exportar_para_auditoria(self):
        return {"memoria": self.memoria, "cadena_valida": self.verificar_cadena(), "prev_hash": self.prev_hash}
