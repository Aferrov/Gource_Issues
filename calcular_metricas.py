import json

# Configuración
REPO_NAME = "Gource"  # Asegúrate de que coincida con el nombre del archivo generado

def calcular_trr():
    json_file = f"{REPO_NAME}_issues_commits.json"
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            issues = json.load(f)
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo {json_file}")
        return

    # Filtrar solo issues CERRADOS (según la definición)
    issues_cerrados = [i for i in issues if i['state'] == 'closed']
    total_cerrados = len(issues_cerrados)
    
    if total_cerrados == 0:
        print("No hay issues cerrados para analizar.")
        return

    # Contar issues con evidencia de trazabilidad (Commits o PRs)
    linked_issues = []
    for issue in issues_cerrados:
        tiene_commits = len(issue.get('related_commits', [])) > 0
        tiene_prs = len(issue.get('related_prs', [])) > 0
        
        # También podemos considerar 'resolution_type' si lo usamos estrictamente
        # pero verificar las listas es más seguro
        if tiene_commits or tiene_prs:
            linked_issues.append(issue)

    total_linked = len(linked_issues)

    # Cálculo TRR
    trr = (total_linked / total_cerrados) * 100

    print("="*60)
    print(f"📊 CÁLCULO DE TASA DE RECUPERACIÓN DE TRAZABILIDAD (TRR)")
    print("="*60)
    print(f"Total Issues Cerrados (|Itotal|): {total_cerrados}")
    print(f"Total Issues Vinculados (|Ilinked|): {total_linked}")
    print("-" * 30)
    print(f"Tasa de Recuperación (TRR): {trr:.2f}%")
    print("="*60)
    
    # Detalle adicional opcional
    print("\nDesglose de Vinculación:")
    solo_commits = len([i for i in linked_issues if i['related_commits'] and not i['related_prs']])
    solo_prs = len([i for i in linked_issues if not i['related_commits'] and i['related_prs']])
    ambos = len([i for i in linked_issues if i['related_commits'] and i['related_prs']])
    
    print(f"  - Solo Commits: {solo_commits}")
    print(f"  - Solo PRs: {solo_prs}")
    print(f"  - Ambos (Commits + PRs): {ambos}")

if __name__ == "__main__":
    calcular_trr()
