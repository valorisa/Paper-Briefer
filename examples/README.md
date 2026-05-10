# Exemples

## DeepSeek-V4

Les fichiers d'exemple dans ce dossier ont été générés à partir du rapport technique DeepSeek-V4 :

- **Source PDF** : <https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf>
- **Traitement OCR** : [OCR Playground de Mistral AI](https://console.mistral.ai/build/document-ai/ocr-playground) (export ZIP avec markdown par page)
- **Commande** : `paper-briefer ocr-playground-download-20260510T130752Z.zip -o examples/`

### Fichiers produits

| Fichier | Contenu |
| ------- | ------- |
| `*-brief.md` | Brief de ~4 155 tokens, prêt pour injection dans un LLM |
| `*-metadata.json` | Métadonnées structurées complètes (46 pages, 22 figures, 49 entrées ToC) |
