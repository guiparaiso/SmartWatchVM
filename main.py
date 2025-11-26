#!/usr/bin/env python3
"""
main.py - Script principal da SmartWatch VM
Versão simplificada sem JSON
"""

import sys
import subprocess
import os
from compiler import Compiler
from vm import VM
from bytecode import disassemble

def compile_and_run(source_file, debug=False):
    """Pipeline completo: código fonte → bytecode → execução"""
    
    print("=" * 60)
    print("SmartWatch Language - Compiler & VM")
    print("=" * 60)
    
    # 1. Verificação sintática com parser C
    print("\n[1/4] Verificação Sintática (Flex/Bison)...")
    
    try:
        # Executa o parser C apenas para verificação
        with open(source_file, 'r') as f:
            source_code = f.read()
        
        result = subprocess.run(
            ['./smartwatch'],
            input=source_code,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            print(f"❌ Erros na verificação sintática:")
            print(result.stderr)
            return False
        
        print("✓ Verificação sintática concluída")
        
    except FileNotFoundError:
        print("❌ Parser 'smartwatch' não encontrado.")
        print("   Compile com: bison -d -o parser.c parser.y && flex -o lexer.c lexer.l && gcc -o smartwatch parser.c lexer.c -lfl")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar parser: {e}")
        return False
    
    # 2. Compilação direta do código fonte
    print("\n[2/4] Compilação para Bytecode...")

    try:
        compiler = Compiler()
        # Compila diretamente do arquivo fonte
        compiler.compile_from_file(source_file)
        print(f"✓ Bytecode gerado: {len(compiler.bytecode)} instruções")
        print(f"  - Variáveis: {compiler.next_var_idx}")
        print(f"  - Strings: {len(compiler.strings)}")
    except Exception as e:
        print(f"❌ Erro na compilação: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 3. Salva bytecode (opcional)
    print("\n[3/4] Salvando Bytecode...")
    
    bytecode_file = source_file.replace('.sw', '.swb')
    compiler.save_bytecode(bytecode_file)
    
    # Mostra desassembly se debug
    # No trecho [3/4] Salvando Bytecode... adicione:
    if debug:  # Temporariamente sempre mostrar
        print("\n=== DISASSEMBLY ===")
        print(disassemble(compiler.bytecode, compiler.strings))
        print("=" * 60)
    
    # 4. Executa na VM
    print("\n[4/4] Executando na VM...")
    print("-" * 60)
    
    try:
        vm = VM(compiler.bytecode, compiler.strings, compiler.next_var_idx)
        vm.run(debug=debug)
        return True
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        import traceback
        traceback.print_exc()
        return False

# ... (o resto do main.py permanece igual)
def run_bytecode(bytecode_file, debug=False):
    """Executa arquivo .swb já compilado"""
    
    print("=" * 60)
    print("SmartWatch VM - Executando bytecode")
    print("=" * 60)
    
    try:
        bytecode, strings, num_vars = Compiler.load_bytecode(bytecode_file)
        
        print(f"\n✓ Bytecode carregado: {bytecode_file}")
        print(f"  - {len(bytecode)} instruções")
        print(f"  - {num_vars} variáveis")
        print(f"  - {len(strings)} strings")
        
        if debug:
            print("\n=== DISASSEMBLY ===")
            print(disassemble(bytecode, strings))
            print("=" * 60)
        
        print("\n=== Executando ===")
        print("-" * 60)
        
        vm = VM(bytecode, strings, num_vars)
        vm.run(debug=debug)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python main.py <arquivo.sw>          # compila e executa")
        print("  python main.py <arquivo.swb>         # executa bytecode")
        print("  python main.py <arquivo.sw> --debug  # modo debug")
        sys.exit(1)
    
    filename = sys.argv[1]
    debug = '--debug' in sys.argv
    
    if not os.path.exists(filename):
        print(f"❌ Arquivo não encontrado: {filename}")
        sys.exit(1)
    
    # Determina tipo de arquivo
    if filename.endswith('.sw'):
        success = compile_and_run(filename, debug)
    elif filename.endswith('.swb'):
        success = run_bytecode(filename, debug)
    else:
        print("❌ Arquivo deve ser .sw (código fonte) ou .swb (bytecode)")
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()