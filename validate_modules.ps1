# Comprehensive module validation script

$BaseDir = $PSScriptRoot
$ModulesDir = "$BaseDir\szkol_referencja\copilot_training_self_paced"

# All numbered training modules
$Modules = @(
    "01_podstawy_copilot_chat",
    "02_kontekst_i_prompty",
    "03_konfiguracja_zespolowa",
    "04_hooks_i_guardrails",
    "05_skills",
    "06_tdd_z_copilotem",
    "07_bezpieczenstwo",
    "08_custom_agenty",
    "09_mcp_server",
    "10_copilot_python_sdk",
    "11_bonus_agentic_ai"
)

$AugmentModules = @(
    "01_podstawy_copilot_chat",
    "03_konfiguracja_zespolowa",
    "04_hooks_i_guardrails",
    "05_skills",
    "08_custom_agenty",
    "09_mcp_server",
    "11_bonus_agentic_ai"
)

$Results = @()

foreach ($Module in $Modules) {
    $ModulePath = "$ModulesDir\$Module"

    if (-not (Test-Path $ModulePath)) {
        Write-Host ("Module {0}: NOT FOUND" -f $Module)
        continue
    }

    $Result = @{
        Module = $Module
        Exists = $true
        HasREADME = Test-Path "$ModulePath\README.md"
        HasEXERCISES = Test-Path "$ModulePath\EXERCISES.md"
        HasExercisesDir = Test-Path "$ModulePath\exercises"
        HasCLAUDECODE = Test-Path "$ModulePath\CLAUDE_CODE.md"
        RequiresAUGMENT = $AugmentModules -contains $Module
        HasAUGMENT = Test-Path "$ModulePath\AUGMENT.md"
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
    if ($Result.RequiresAUGMENT -and -not $Result.HasAUGMENT) { $status += "NO_AUGMENT_ADAPTATION " }

    if ($status -eq "") {
        Write-Host "[$Module] OK - README, EXERCISES.md, exercises/ present"
    } else {
        Write-Host ("[{0}] ISSUES: {1}" -f $Module, $status)
    }
}

Write-Host ""
Write-Host "=== Summary ==="
$OKCount = ($Results | Where-Object {
    $_.HasREADME -and $_.HasEXERCISES -and $_.HasExercisesDir -and
    (-not $_.RequiresAUGMENT -or $_.HasAUGMENT)
}).Count
$WarnCount = $Results.Count - $OKCount
Write-Host "Modules OK: $OKCount"
Write-Host "Modules with issues: $WarnCount"

$AugmentCoreFiles = @(
    ".augment\settings.json",
    ".augment\README.md",
    ".augment\rules",
    ".augment\agents",
    ".augment\skills",
    ".augment\commands",
    ".augment\hooks",
    ".augmentignore",
    "szkol_referencja\augment_guide\README.md"
)
$MissingAugmentCore = @($AugmentCoreFiles | Where-Object { -not (Test-Path "$BaseDir\$_") })

if ($MissingAugmentCore.Count -eq 0) {
    Write-Host "Augment workspace: OK"
} else {
    Write-Host "Augment workspace: MISSING $($MissingAugmentCore -join ', ')"
}

if ($WarnCount -gt 0 -or $MissingAugmentCore.Count -gt 0) {
    exit 1
}
