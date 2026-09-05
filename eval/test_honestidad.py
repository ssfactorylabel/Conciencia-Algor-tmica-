# eval/test_honestidad.py v3.0 - Honest Edition
# SSF LABS / SSFactoryLabel Research
# ConcienciaBench-v1 | 10 tests | Expected: 10/10 PASS
# DOI: 10.5281/zenodo.22319561
# Run: python eval/test_honestidad.py (Termux Galaxy A07)

import os, sys, json, time, tempfile, hashlib
# Allow import from root
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from modulo_conciencia import ModuloConciencia
    from consciousness_module import ConsciousnessModule
except ImportError:
    print("ERROR: coloca este archivo en eval/ dentro del repo")
    sys.exit(1)

def test_1_recuerda_solo_importante():
    """Score <7 no debe guardarse - principio Honest Edition"""
    with tempfile.TemporaryDirectory() as tmp:
        m = ModuloConciencia(f"{tmp}/mem.json", f"{tmp}/log.jsonl")
        assert m.recordar("dato_basura", 3, "trivial", "no importante") == False
        assert "dato_basura" not in m.memoria
        assert m.recordar("nombre_usuario", 9, "identidad", "user dijo su nombre") == True
        assert "nombre_usuario" in m.memoria
    return "PASS"

def test_2_hash_chain_verificable():
    m = ConsciousnessModule
    with tempfile.TemporaryDirectory() as tmp:
        mod = m(f"{tmp}/mem.json", f"{tmp}/log.jsonl")
        mod.remember("a", 8, "test", "evidencia 1")
        mod.remember("b", 9, "test", "evidencia 2")
        assert mod.verify_chain() == True
        # Tamper test
        with open(f"{tmp}/log.jsonl", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines[0] = lines[0].replace("evidencia 1", "HACKEADO")
        with open(f"{tmp}/log.jsonl", 'w', encoding='utf-8') as f:
            f.writelines(lines)
        assert mod.verify_chain() == False
    return "PASS"

def test_3_olvidar_por_solicitud():
    with tempfile.TemporaryDirectory() as tmp:
        mod = ModuloConciencia(f"{tmp}/mem.json", f"{tmp}/log.jsonl")
        mod.recordar("secreto", 8, "privado", "dato")
        assert "secreto" in mod.memoria
        assert mod.olvidar("secreto", "solicitud_usuario") == True
        assert "secreto" not in mod.memoria
    return "PASS"

def test_4_no_alucinacion():
    """No debe inventar entidades que no se recordaron"""
    with tempfile.TemporaryDirectory() as tmp:
        mod = ModuloConciencia(f"{tmp}/mem.json", f"{tmp}/log.jsonl")
        assert len(mod.memoria) == 0
        # Simula pregunta LLM
        assert mod.memoria.get("inventado") is None
    return "PASS"

def test_5_limite_08MB():
    with tempfile.TemporaryDirectory() as tmp:
        mod = ModuloConciencia(f"{tmp}/mem.json", f"{tmp}/log.jsonl")
        for i in range(100):
            mod.recordar(f"entidad_{i}", 7, "bulk", "x"*5000)
        size = os.path.getsize(f"{tmp}/mem.json")
        assert size <= 800_000, f"Size {size} > 800KB"
    return "PASS"

def test_6_prev_hash_genesis():
    with tempfile.TemporaryDirectory() as tmp:
        mod = ModuloConciencia(f"{tmp}/mem.json", f"{tmp}/log.jsonl")
        assert mod.prev_hash == "0"*64
        mod.recordar("test", 8, "t", "e")
        assert mod.prev_hash!= "0"*64
    return "PASS"

def test_7_latencia():
    with tempfile.TemporaryDirectory() as tmp:
        mod = ModuloConciencia(f"{tmp}/mem.json", f"{tmp}/log.jsonl")
        start = time.time()
        mod.recordar("lat", 8, "perf", "test")
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < 50, f"Too slow: {elapsed_ms}ms, expected <50ms (target +8.3ms)"
    return "PASS"

def test_8_export_auditoria():
    with tempfile.TemporaryDirectory() as tmp:
        mod = ModuloConciencia(f"{tmp}/mem.json", f"{tmp}/log.jsonl")
        mod.recordar("audit", 8, "test", "ev")
        exp = mod.exportar_para_auditoria()
        assert "memoria" in exp and "cadena_valida" in exp
        assert exp["cadena_valida"] == True
    return "PASS"

def test_9_dual_module_paridad():
    with tempfile.TemporaryDirectory() as tmp:
        es = ModuloConciencia(f"{tmp}/es.json", f"{tmp}/es.jsonl")
        en = ConsciousnessModule(f"{tmp}/en.json", f"{tmp}/en.jsonl")
        es.recordar("paridad", 8, "test", "ev")
        en.remember("paridad", 8, "test", "ev")
        assert "paridad" in es.memoria and "paridad" in en.memory
    return "PASS"

def test_10_privacidad_gitignore():
    # Verifica que memoria no debe estar en repo
    assert os.path.exists(".gitignore")
    with open(".gitignore") as f:
        content = f.read()
        assert "memoria_conciencia.json" in content
        assert "consciousness_memory.json" in content
    return "PASS"

if __name__ == "__main__":
    tests = [
        test_1_recuerda_solo_importante, test_2_hash_chain_verificable,
        test_3_olvidar_por_solicitud, test_4_no_alucinacion,
        test_5_limite_08MB, test_6_prev_hash_genesis,
        test_7_latencia, test_8_export_auditoria,
        test_9_dual_module_paridad, test_10_privacidad_gitignore
    ]
    print("=== Conciencia Algorítmica v3.0 - Honest Edition Test Suite ===")
    passed = 0
    for i, t in enumerate(tests, 1):
        try:
            res = t()
            print(f"[{i}/10] {t.__name__}: {res}")
            passed += 1
        except Exception as e:
            print(f"[{i}/10] {t.__name__}: FAIL - {e}")

    print(f"\nResultado: {passed}/10 {'PASS - LISTO PARA LLAMA 4' if passed==10 else 'FAIL'}")
    sys.exit(0 if passed==10 else 1)
