#!/usr/bin/env bash
# Téléchargement facultatif de la page d'origine depuis un réseau qui y a accès.
set -euo pipefail

source_url="${SOURCE_URL:-https://www.allianz.fr/assurances-professionnels-entreprises.html}"
output_dir="${OUTPUT_DIR:-original}"
entry_name="assurances-professionnels-entreprises.html"

if ! command -v wget >/dev/null 2>&1; then
  printf 'GNU wget est nécessaire pour télécharger la page originale.\n' >&2
  exit 1
fi
if [[ -e "$output_dir" ]]; then
  printf 'Le dossier « %s » existe déjà. Choisissez un autre dossier avec OUTPUT_DIR ou supprimez-le après vérification.\n' "$output_dir" >&2
  exit 1
fi

mkdir -p "$(dirname "$output_dir")"
temp_dir="$(mktemp -d "${output_dir}.tmp.XXXXXX")"
cleanup() { rm -rf -- "$temp_dir"; }
trap cleanup EXIT

printf 'Téléchargement de %s et de ses ressources accessibles…\n' "$source_url"
# -p récupère les ressources nécessaires à la page, pas les pages liées.
# Les ressources de domaines tiers et les services dynamiques peuvent rester distants.
if ! wget --page-requisites --convert-links --adjust-extension \
  --no-host-directories --restrict-file-names=windows \
  --directory-prefix="$temp_dir" --timeout=20 --tries=2 \
  --user-agent='Mozilla/5.0 (compatible; local-page-copy/1.0)' "$source_url"; then
  printf '\nTéléchargement impossible ou incomplet. Vérifiez la connexion et les éventuelles protections du site.\n' >&2
  exit 1
fi

entry="$temp_dir/$entry_name"
if [[ ! -s "$entry" ]] || grep -Eiq '<title>Just a moment|cf_chl_opt|cdn-cgi/challenge-platform' "$entry"; then
  printf '\nLa page originale n’a pas pu être récupérée (page absente ou contrôle anti-robot).\n' >&2
  exit 1
fi

mv -- "$temp_dir" "$output_dir"
trap - EXIT
printf '\nPage téléchargée : %s/%s\n' "$output_dir" "$entry_name"
printf 'Certaines ressources et fonctions dynamiques peuvent toujours nécessiter Internet.\n'
