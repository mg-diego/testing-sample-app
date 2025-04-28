#!/bin/bash

# Set default values for variables if not set
DB_NAME="testing-sample-app"
DB_USER=${DB_USER:-user}
DB_HOST=${DB_HOST:-postgres}
DB_PASSWORD=${DB_PASSWORD:-password}
DB_PORT=${DB_PORT:-5432}

# Set the password for the session
export PGPASSWORD="$DB_PASSWORD"

# Step 2: Check if the table exists
TABLE_EXISTS=$(psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -t -c "SELECT to_regclass('public.languages');")

if [ "$TABLE_EXISTS" = "languages" ]; then
  echo "Table 'languages' already exists."
else
  echo "Creating table 'languages'..."
  psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "CREATE TABLE public.languages (
    language VARCHAR PRIMARY KEY,
    active BOOLEAN NOT NULL DEFAULT false
  );"

  # Optional: Add a partial unique index to enforce only one active language
  psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "CREATE UNIQUE INDEX one_active_language ON public.languages (active) WHERE active;"
fi

# Step 3: List of required languages, and which one should be active
LANGUAGES=("en" "es" "fr" "pt" "jp")
ACTIVE_LANG="en"

# Step 4: Check each language
for LANG in "${LANGUAGES[@]}"; do
  EXISTS=$(psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -t -c "SELECT 1 FROM public.languages WHERE language = '$LANG' LIMIT 1;")
  
  if [ "$EXISTS" = "1" ]; then
    echo "Language '$LANG' already exists."
  else
    IS_ACTIVE="false"
    if [ "$LANG" = "$ACTIVE_LANG" ]; then
      IS_ACTIVE="true"
    fi
    echo "Inserting language '$LANG' (active: $IS_ACTIVE)..."
    psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "INSERT INTO public.languages (language, active) VALUES ('$LANG', $IS_ACTIVE);"
  fi
done

# Step 5: Make sure only the desired language is active
psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "UPDATE public.languages SET active = false WHERE language != '$ACTIVE_LANG';"
psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "UPDATE public.languages SET active = true WHERE language = '$ACTIVE_LANG';"

# Unset the password for security
unset PGPASSWORD
