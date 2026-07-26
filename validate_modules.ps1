# Comprehensive module validation script

$BaseDir = $PSScriptRoot
$ModulesDir = "$BaseDir\szkol_referencja\copilot_training_self_paced"

# Modules to validate (skip 09)
$Modules = @(
    "01_podstawy_copilot_chat",
    "02_kontekst_i_prompty",
    "03_konfiguracja_zespolowa",
    "04_hooks_i_guardrails",
    "05_skills",
    "06_tdd_z_copilotem",
    "07_bezpieczenstwo",
    "08_custom_agenty",
    "10_copilot_python_sdk"
)

$Results = @()

foreach ($Module in $Modules) {
    $ModulePath = "$ModulesDir\$Module"

    if (-not (Test-Path $ModulePath)) {
        Write-Host "Module ${Module}: NOT FOUND"
        continue
    }

    $Result = @{
        Module = $Module
        Exists = $true
        HasREADME = Test-Path "$ModulePath\README.md"
        HasEXERCISES = Test-Path "$ModulePath\EXERCISES.md"
        HasExercisesDir = Test-Path "$ModulePath\exercises"
        HasCLAUDECODE = Test-Path "$ModulePath\CLAUDE_CODE.md"
        ExerciseFiles = @()
    }

    # Check exercise files
    if ($Result.HasEXERCISES) {
        $Content = Get-Content "$ModulePath\EXERCISES.md" -Raw
        $ExerciseMatches = [regex]::Matches($Content, '\[ex_(\d+[a-z]?)\]')
        foreach ($Match in $ExerciseMatches) {
            $ExNum = $Match.Groups[1].Value
            $Result.ExerciseFiles += $ExNum
        }
    }

    $Results += $Result

    # Status summary
    $status = ""
    if (-not $Result.HasREADME) { $status += "NO_README " }
    if (-not $Result.HasEXERCISES) { $status += "NO_EXERCISES " }
    if (-not $Result.HasExercisesDir) { $status += "NO_EXERCISES_DIR " }

    if ($status -eq "") {
        Write-Host "[$Module] OK - README, EXERCISES.md, exercises/ present"
    } else {
        Write-Host "[$Module] ISSUES: $status"
    }
}

Write-Host ""
Write-Host "=== Summary ==="
$OKCount = ($Results | Where-Object { $_.HasREADME -and $_.HasEXERCISES -and $_.HasExercisesDir }).Count
$WarnCount = ($Results | Where-Object { -not ($_.HasREADME -and $_.HasEXERCISES -and $_.HasExercisesDir) }).Count
Write-Host "Modules OK: $OKCount"
Write-Host "Modules with issues: $WarnCount"
