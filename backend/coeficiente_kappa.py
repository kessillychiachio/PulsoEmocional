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
    melkes = _load_table("avaliacoes_melkes.xlsx", "avaliacoes_melkes.csv")

    if base is None or danilo is None or melkes is None:
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

    if "Texto" not in danilo.columns or ("Avaliação Humana (Danilo)" not in danilo.columns and "Avaliacao_Danilo" not in danilo.columns):
        print("ERRO: A planilha do Danilo deve conter as colunas 'Texto' e 'Avaliação Humana (Danilo)'.")
        return
    if "Texto" not in melkes.columns or ("Avaliação Humana (Melkes)" not in melkes.columns and "Avaliacao_Melkes" not in melkes.columns):
        print("ERRO: A planilha do Melkes deve conter as colunas 'Texto' e 'Avaliação Humana (Melkes)'.")
        return

    if "Avaliação Humana (Danilo)" in danilo.columns:
        danilo = danilo.rename(columns={"Avaliação Humana (Danilo)": "Avaliacao_Danilo"})
    if "Avaliação Humana (Melkes)" in melkes.columns:
        melkes = melkes.rename(columns={"Avaliação Humana (Melkes)": "Avaliacao_Melkes"})

    base["Texto"] = base["Texto"].astype(str)
    danilo["Texto"] = danilo["Texto"].astype(str)
    melkes["Texto"] = melkes["Texto"].astype(str)

    df = base.merge(danilo[["Texto", "Avaliacao_Danilo"]], on="Texto", how="left")
    df = df.merge(melkes[["Texto", "Avaliacao_Melkes"]], on="Texto", how="left")

    df["Polaridade"] = _normalize_label(df["Polaridade"])
    df["Avaliacao_Danilo"] = _normalize_label(df["Avaliacao_Danilo"]) if "Avaliacao_Danilo" in df.columns else ""
    df["Avaliacao_Melkes"] = _normalize_label(df["Avaliacao_Melkes"]) if "Avaliacao_Melkes" in df.columns else ""

    print("Amostra consolidada:")
    print(df.head())
    print("-" * 50)

    df_k = df[(df["Avaliacao_Danilo"] != "") & (df["Avaliacao_Melkes"] != "")]
    if df_k.empty:
        print("ERRO: Nenhuma avaliação humana preenchida nas duas planilhas.")
        return

    kappa_ia_danilo = cohen_kappa_score(df_k["Polaridade"], df_k["Avaliacao_Danilo"])
    kappa_ia_melkes = cohen_kappa_score(df_k["Polaridade"], df_k["Avaliacao_Melkes"])
    kappa_danilo_melkes = cohen_kappa_score(df_k["Avaliacao_Danilo"], df_k["Avaliacao_Melkes"])

    print(f"Coeficiente de Kappa (IA vs. Danilo): {kappa_ia_danilo:.4f} -> {interpretar_kappa(kappa_ia_danilo)}")
    print(f"Coeficiente de Kappa (IA vs. Melkes): {kappa_ia_melkes:.4f} -> {interpretar_kappa(kappa_ia_melkes)}")
    print(f"Coeficiente de Kappa (Danilo vs. Melkes): {kappa_danilo_melkes:.4f} -> {interpretar_kappa(kappa_danilo_melkes)}")

    try:
        df.to_excel("resultados_consolidados_finais.xlsx", index=False, engine="openpyxl")
        print("Planilha 'resultados_consolidados_finais.xlsx' criada.")
    except Exception:
        df.to_csv("resultados_consolidados_finais.csv", index=False, encoding="utf-8")
        print("Planilha 'resultados_consolidados_finais.csv' criada (fallback).")


if __name__ == "__main__":
    consolidar_e_calcular_kappa()