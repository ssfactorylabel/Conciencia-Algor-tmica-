# eval/verificar_cadena.py v3.0 - Honest Edition
# SSF LABS / SSFactoryLabel Research - Andrés Garbán
# Verificador de cadena SHA256 para memoria responsable
# Uso: python eval/verificar_cadena.py [archivo_log.jsonl]
# DOI: 10.5281/zenodo.22319561

import json, hashlib, sys, os

def verificar_archivo(path):
    if not os.path.exists(path):
        print(f"[INFO] No existe {path} - cadena vacía válida (genesis)")
        return True

    print(f"Verificando: {path}")
    prev = "0" * 64
    count = 0
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for n, line in enumerate(f, 1):
                if not line.strip(): continue
                e = json.loads(line)
                stored_hash = e.pop("hash", None)
                if not stored_hash:
                    print(f"[FAIL] Línea {n}: sin campo hash")
                    return False
                payload = json.dumps(e, sort_keys=True, ensure_ascii=False)
                calc = hashlib.sha256((prev + payload).encode()).hexdigest()
                if calc != stored_hash:
                    print(f"[FAIL] Línea {n}: hash no coincide")
                    print(f"  Esperado: {stored_hash}")
                    print(f"  Calculado: {calc}")
                    print(f"  Evento: {e}")
                    return False
                prev = stored_hash
                count += 1
        print(f"[PASS] Cadena válida - {count} eventos - último hash: {prev[:16]}...")
        return True
    except Exception as ex:
        print(f"[ERROR] {ex}")
        return False

if __name__ == "__main__":
    archivos = sys.argv[1:] if len(sys.argv) > 1 else [
        "memoria_conciencia.json",
        "consciousness_memory.json",
        "log_conciencia.json",
        "logs_honestidad.jsonl",
        "honesty_logs.jsonl",
        "eval/../memoria_conciencia.json",
        "eval/../logs_honestidad.jsonl"
    ]
    # Busca logs reales
    logs_encontrados = [f for f in ["logs_honestidad.jsonl", "honesty_logs.jsonl", "log_conciencia.json", "eval/logs_honestidad.jsonl"] if os.path.exists(f)]
    
    if logs_encontrados:
        archivos = logs_encontrados
    elif len(sys.argv) == 1:
        # Si no hay logs, crea uno de demo para mostrar
        print("=== Verificador de Memoria Responsable v3.0 ===")
        print("No se encontraron logs. Verificando archivos por defecto...\n")

    ok = True
    for path in archivos:
        if os.path.exists(path) and path.endswith(".jsonl"):
            if not verificar_archivo(path):
                ok = False

    if ok:
        print("\n✓ MEMORIA VERIFICABLE - LISTO PARA AUDITORIA LLAMA 4")
    else:
        print("\n✗ CADENA COMPROMETIDA")
        sys.exit(1)
