import pandas as pd
from sklearn.metrics import cohen_kappa_score


def _load_table(xlsx: str, csv: str | None = None) -> pd.DataFrame | None:
    try:
        return pd.read_excel(xlsx)
    except FileNotFoundError:
        if csv:
            try:
                return pd.read_csv(csv)
            except FileNotFoundError:
                return None
        return None


def _normalize_label(s: pd.Series) -> pd.Series:
    return s.fillna("").astype(str).str.strip().str.upper()


def interpretar_kappa(kappa_score: float) -> str:
    if kappa_score >= 0.81:
        return "Quase Perfeita"
    if kappa_score >= 0.61:
        return "Substancial"
    if kappa_score >= 0.41:
        return "Moderada"
    if kappa_score >= 0.21:
        return "Razoável"
    if kappa_score >= 0.01:
        return "Leve"
    return "Ruim"


def consolidar_e_calcular_kappa():
    base = _load_table("resultados_da_ia.xlsx", "resultados_da_ia.csv")
    danilo = _load_table("avaliacoes_danilo.xlsx", "avaliacoes_danilo.csv")
    melques = _load_table("avaliacoes_melques.xlsx", "avaliacoes_melques.csv")

    if base is None or danilo is None or melques is None:
        print("ERRO: Arquivos necessários não encontrados. Gere as planilhas e preencha as avaliações.")
        return

    if "Texto" not in base.columns:
        if "Mensagem Coletada" in base.columns:
            base["Texto"] = base["Mensagem Coletada"].astype(str)
        else:
            print("ERRO: A planilha base precisa conter a coluna 'Texto' ou 'Mensagem Coletada'.")
            return

    if "Polaridade" not in base.columns:
        if "Sentimento da IA" in base.columns:
            base["Polaridade"] = base["Sentimento da IA"].astype(str)
        else:
            print("ERRO: A planilha base precisa conter a coluna 'Polaridade' ou 'Sentimento da IA'.")
            return

    if "Texto" not in danilo.columns or ("Avaliação Humana (danilo)" not in danilo.columns and "Avaliacao_danilo" not in danilo.columns):
        print("ERRO: A planilha do danilo deve conter as colunas 'Texto' e 'Avaliação Humana (danilo)'.")
        return
    if "Texto" not in melques.columns or ("Avaliação Humana (melques)" not in melques.columns and "Avaliacao_melques" not in melques.columns):
        print("ERRO: A planilha do melques deve conter as colunas 'Texto' e 'Avaliação Humana (melques)'.")
        return

    if "Avaliação Humana (danilo)" in danilo.columns:
        danilo = danilo.rename(columns={"Avaliação Humana (danilo)": "Avaliacao_danilo"})
    if "Avaliação Humana (melques)" in melques.columns:
        melques = melques.rename(columns={"Avaliação Humana (melques)": "Avaliacao_melques"})

    base["Texto"] = base["Texto"].astype(str)
    danilo["Texto"] = danilo["Texto"].astype(str)
    melques["Texto"] = melques["Texto"].astype(str)

    df = base.merge(danilo[["Texto", "Avaliacao_danilo"]], on="Texto", how="left")
    df = df.merge(melques[["Texto", "Avaliacao_melques"]], on="Texto", how="left")

    df["Polaridade"] = _normalize_label(df["Polaridade"])
    df["Avaliacao_danilo"] = _normalize_label(df["Avaliacao_danilo"]) if "Avaliacao_danilo" in df.columns else ""
    df["Avaliacao_melques"] = _normalize_label(df["Avaliacao_melques"]) if "Avaliacao_melques" in df.columns else ""

    print("Amostra consolidada:")
    print(df.head())
    print("-" * 50)

    df_k = df[(df["Avaliacao_danilo"] != "") & (df["Avaliacao_melques"] != "")]
    if df_k.empty:
        print("ERRO: Nenhuma avaliação humana preenchida nas duas planilhas.")
        return

    kappa_ia_danilo = cohen_kappa_score(df_k["Polaridade"], df_k["Avaliacao_danilo"])
    kappa_ia_melques = cohen_kappa_score(df_k["Polaridade"], df_k["Avaliacao_melques"])
    kappa_danilo_melques = cohen_kappa_score(df_k["Avaliacao_danilo"], df_k["Avaliacao_melques"])

    print(f"Coeficiente de Kappa (IA vs. danilo): {kappa_ia_danilo:.4f} -> {interpretar_kappa(kappa_ia_danilo)}")
    print(f"Coeficiente de Kappa (IA vs. melques): {kappa_ia_melques:.4f} -> {interpretar_kappa(kappa_ia_melques)}")
    print(f"Coeficiente de Kappa (danilo vs. melques): {kappa_danilo_melques:.4f} -> {interpretar_kappa(kappa_danilo_melques)}")

    try:
        df.to_excel("resultados_consolidados_finais.xlsx", index=False, engine="openpyxl")
        print("Planilha 'resultados_consolidados_finais.xlsx' criada.")
    except Exception:
        df.to_csv("resultados_consolidados_finais.csv", index=False, encoding="utf-8")
        print("Planilha 'resultados_consolidados_finais.csv' criada (fallback).")


if __name__ == "__main__":
    consolidar_e_calcular_kappa()