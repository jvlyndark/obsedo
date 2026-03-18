{{/*
Expand the name of the chart.
*/}}
{{- define "obsedo.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "obsedo.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "obsedo.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Construct the DATABASE_URL from postgres values
*/}}
{{- define "obsedo.databaseUrl" -}}
{{- printf "postgresql://%s:%s@postgres:5432/%s" .Values.postgres.user .Values.postgres.password .Values.postgres.database }}
{{- end }}
