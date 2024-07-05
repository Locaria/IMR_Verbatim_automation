
# ##Updated the script tp set specific run times for each sheet
# #1: 1H0iwabIZGp2VWYE_sblFfYaiDGlFX4xK0lR1KDAD9Cc - NRG at xx:30;
# #2: 1a_VWRE5tR0ISCvyw-UBt2vpc3X2SSYJx8H_6HTLNBpQ - HIA at XX:40;
# #3: 1vuXdi46puy-QaCjjghPQf8yc9VZ751Bw8RiY97RgHVc - HarrisX at XX:50.

# # Define paths for Python interpreter and script files
# $pythonInterpreterPath = "C:\Users\MrMagoo\anaconda3\python.exe"
# $hourlyScriptPath_Sheet1 = Join-Path -Path $PSScriptRoot -ChildPath "plunet_pulls\IH_linguist_ratecards.py"
# $hourlyScriptPath_Sheet2 = Join-Path -Path $PSScriptRoot -ChildPath "plunet_pulls\IH_VM_daily_updates.py"
# $hourlyScriptPath_Sheet3 = Join-Path -Path $PSScriptRoot -ChildPath "plunet_pulls\IH_monthly_updates.py"
# $hourlyScriptPath_IMC = Join-Path -Path $PSScriptRoot -ChildPath "IMR_Cost_trackers\ipynb_checkpoints\IMRCostTrackers.py"

# $currentTime = Get-Date # Get the current time

# # Initialize the last daily run time based on the current time
# if ($currentTime.TimeOfDay -ge [timespan]::FromHours(5)) {
#     $lastDailyRun = [datetime]::Today.AddHours(5)
# } else {
#     $lastDailyRun = [datetime]::Today.AddDays(-1).AddHours(5)
# }

# $lastHourlyRun = [datetime]::MinValue # Initialize last run times to min value

# $nextRunTime_Sheet1 = [datetime]::Today.AddHours($currentTime.Hour).AddMinutes(30)
# if ($currentTime.Minute -ge 30) {
#     $nextRunTime_Sheet1 = $nextRunTime_Sheet1.AddHours(1)
# }

# $nextRunTime_Sheet2 = [datetime]::Today.AddHours($currentTime.Hour).AddMinutes(40)
# if ($currentTime.Minute -ge 40) {
#     $nextRunTime_Sheet2 = $nextRunTime_Sheet2.AddHours(1)
# }

# $nextRunTime_Sheet3 = [datetime]::Today.AddHours($currentTime.Hour).AddMinutes(50)
# if ($currentTime.Minute -ge 50) {
#     $nextRunTime_Sheet3 = $nextRunTime_Sheet3.AddHours(1)
# }

# $nextDailyRunTime = [datetime]::Today.AddHours(5)
# if ($currentTime.TimeOfDay -ge [timespan]::FromHours(5)) {
#     $nextDailyRunTime = $nextDailyRunTime.AddDays(1)
# }

# # Initialize the last monthly run time
# $lastMonthlyRun = Get-Date -Year $currentTime.Year -Month $currentTime.Month -Day 1 -Hour 7 -Minute 0 -Second 0
# $nextMonthlyRunTime = $lastMonthlyRun.AddMonths(1) # Schedule the next monthly run

# Write-Host "$($currentTime.ToString()) - Script initialization complete. Entering main loop."
# Write-Host "$($currentTime.ToString()) - Sheet 1 Script - Next run scheduled for: $($nextRunTime_Sheet1)"
# Write-Host "$($currentTime.ToString()) - Sheet 2 Script - Next run scheduled for: $($nextRunTime_Sheet2)"
# Write-Host "$($currentTime.ToString()) - Sheet 3 Script - Next run scheduled for: $($nextRunTime_Sheet3)"
# Write-Host "$($currentTime.ToString()) - Daily Script - Next run scheduled for: $($nextDailyRunTime)"
# Write-Host "$($currentTime.ToString()) - Monthly Script - Next run scheduled for: $($nextMonthlyRunTime)"

# while ($true) { # Enter an infinite loop

#     $currentTime = Get-Date # Update the current time

#     # Check if it's time to run the Sheet 1 script
#     if ($currentTime -ge $nextRunTime_Sheet1) {
        
#         Write-Host "$($currentTime.ToString()) Running the Sheet 1 script..."
#         & $pythonInterpreterPath $hourlyScriptPath_Sheet1  # Run the Sheet 1 script
#         Write-Host "$($currentTime.ToString()) - Sheet 1 script completed."
    
#         $lastRunTime_Sheet1 = $currentTime  # Update the last run time
#         $nextRunTime_Sheet1 = $lastRunTime_Sheet1.Date.AddHours($lastRunTime_Sheet1.Hour + 1).AddMinutes(30)
#     }

#     # Check if it's time to run the Sheet 2 script
#     if ($currentTime -ge $nextRunTime_Sheet2) {
        
#         Write-Host "$($currentTime.ToString()) - Running the Sheet 2 script..."
#         & $pythonInterpreterPath $hourlyScriptPath_Sheet2  # Run the Sheet 2 script
#         Write-Host "$($currentTime.ToString()) - Sheet 2 script completed."
    
#         $lastRunTime_Sheet2 = $currentTime  # Update the last run time for Sheet 2 script
#         $nextRunTime_Sheet2 = $lastRunTime_Sheet2.Date.AddHours($lastRunTime_Sheet2.Hour + 1).AddMinutes(40)
#     }

#     # Check if it's time to run the Sheet 3 script
#     if ($currentTime -ge $nextRunTime_Sheet3) {
        
#         Write-Host "$($currentTime.ToString()) - Running the Sheet 3 script..."
#         & $pythonInterpreterPath $hourlyScriptPath_Sheet3  # Run the Sheet 3 script
#         Write-Host "$($currentTime.ToString()) - Sheet 3 script completed."
    
#         $lastRunTime_Sheet3 = $currentTime  # Update the last run time for Sheet 3 script
#         $nextRunTime_Sheet3 = $lastRunTime_Sheet3.Date.AddHours($lastRunTime_Sheet3.Hour + 1).AddMinutes(50)
#     }

#     # Check if it's time to run the daily script
#     if ($currentTime.Date -eq $lastDailyRun.Date.AddDays(1) -and $currentTime.TimeOfDay -ge [timespan]::FromHours(5)) {

#         Write-Host "$($currentTime.ToString()) - Running the daily script..."
#         & $pythonInterpreterPath $dailyScriptPath  # Run the daily script
#         Write-Host "$($currentTime.ToString()) - Daily script completed."
    
#         $lastDailyRun = [datetime]::Today.AddHours(5)  # Update the last daily run time
#     }

#     # Check if it's time to run the monthly script
#     if ($currentTime -ge $nextMonthlyRunTime -and $currentTime.Day -eq 1 -and $currentTime.Hour -eq 7) {

#         Write-Host "$($currentTime.ToString()) - Running the monthly script..."
#         & $pythonInterpreterPath $monthlyScriptPath  # Run the monthly script
#         Write-Host "$($currentTime.ToString()) - Monthly script completed."
    
#         $lastMonthlyRun = $currentTime  # Update the last run time
#         $nextMonthlyRunTime = $lastMonthlyRun.AddMonths(1) # Schedule the next monthly run
#     }
    
#     Start-Sleep -Seconds 30 # Sleep for a while before checking again
# }


# Define paths for Python interpreter and script files
$pythonInterpreterPath = "C:\Users\MrMagoo\anaconda3\python.exe"
$hourlyScriptPath = Join-Path -Path $PSScriptRoot -ChildPath "plunet_pulls\IH_linguist_ratecards.py"
$dailyScriptPath = Join-Path -Path $PSScriptRoot -ChildPath "plunet_pulls\IH_VM_daily_updates.py"
$monthlyScriptPath = Join-Path -Path $PSScriptRoot -ChildPath "plunet_pulls\IH_monthly_updates.py"
$hourlyScriptPath_IMC = Join-Path -Path $PSScriptRoot -ChildPath "IMR_Cost_trackers\ipynb_checkpoints\IMRCostTrackers.py"
$verbatimScriptPath = Join-Path -Path $PSScriptRoot -ChildPath "IMR\verbetim_auto\verbatim_trackers.py" 

$currentTime = Get-Date # Get the current time

# Initialize the last daily run time based on the current time
if ($currentTime.TimeOfDay -ge [timespan]::FromHours(5)) {
    $lastDailyRun = [datetime]::Today.AddHours(5)
} else {
    $lastDailyRun = [datetime]::Today.AddDays(-1).AddHours(5)
}

$lastHourlyRun = [datetime]::MinValue # Initialize last run times to min value
$nextHourlyRunTime = [datetime]::Today.AddHours($currentTime.Hour).AddMinutes(7)
if ($currentTime.Minute -ge 7) {
    $nextHourlyRunTime = $nextHourlyRunTime.AddHours(1)
}

$nextHourlyRunTime_IMC = [datetime]::Today.AddHours($currentTime.Hour).AddMinutes(30)
if ($currentTime.Minute -ge 30) {
    $nextHourlyRunTime_IMC = $nextHourlyRunTime_IMC.AddHours(1)
}

$nextDailyRunTime = [datetime]::Today.AddHours(5)
if ($currentTime.TimeOfDay -ge [timespan]::FromHours(5)) {
    $nextDailyRunTime = $nextDailyRunTime.AddDays(1)
}

# Initialize the last monthly run time
$lastMonthlyRun = Get-Date -Year $currentTime.Year -Month $currentTime.Month -Day 1 -Hour 7 -Minute 0 -Second 0
$nextMonthlyRunTime = $lastMonthlyRun.AddMonths(1) # Schedule the next monthly run

#Update Verbatim

# Atualização: Inicialização dos horários de execução do script verbatim
$londonTimeZone = [System.TimeZoneInfo]::FindSystemTimeZoneById("GMT Standard Time")
$currentLondonTime = [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([datetime]::Now, $londonTimeZone.Id)

$nextRunTimeNoon = [datetime]::Today.AddHours(12) # Noon
$nextRunTimeMidnight = [datetime]::Today.AddHours(24) # Midnight

if ($currentLondonTime.Hour -ge 12) {
    $nextRunTimeNoon = $nextRunTimeNoon.AddDays(1)
}

if ($currentLondonTime.Hour -ge 0 -and $currentLondonTime.Hour -lt 12) {
    $nextRunTimeMidnight = $nextRunTimeMidnight.AddDays(1)
}

Write-Host "$($currentTime.ToString()) - Script initialization complete. Entering main loop."
Write-Host "$($currentTime.ToString()) - Hourly Script - Next run scheduled for: $($nextHourlyRunTime)"
Write-Host "$($currentTime.ToString()) - Hourly Script IMC - Next run scheduled for: $($nextHourlyRunTime_IMC)"
Write-Host "$($currentTime.ToString()) - Daily Script - Next run scheduled for: $($nextDailyRunTime)"
Write-Host "$($currentTime.ToString()) - Monthly Script - Next run scheduled for: $($nextMonthlyRunTime)"
Write-Host "$($currentTime.ToString()) - Verbatim Script - Next run at noon scheduled for: $($nextRunTimeNoon)"  # Verbatim 12am
Write-Host "$($currentTime.ToString()) - Verbatim Script - Next run at midnight scheduled for: $($nextRunTimeMidnight)"  # Verbatim 12pm

while ($true) { # Enter an infinite loop

    $currentTime = Get-Date # Update the current time
    $currentLondonTime = [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([datetime]::Now, $londonTimeZone.Id) #London Time - IMR request

    # Check if it's time to run the hourly script
    if ($currentTime -ge $nextHourlyRunTime) {
        
        Write-Host "$($currentTime.ToString()) Running the hourly VM script..."
        & $pythonInterpreterPath $hourlyScriptPath  # Run the hourly VM/linguist script
        Write-Host "$($currentTime.ToString()) - Hourly VM script completed."
    
        $lastHourlyRun = $currentTime  # Update the last run time
        $nextHourlyRunTime = $lastHourlyRun.Date.AddHours($lastHourlyRun.Hour + 1).AddMinutes(7)
    }

    # Check if it's time to run the hourly IMC script
    if ($currentTime -ge $nextHourlyRunTime_IMC) {
        
        Write-Host "$($currentTime.ToString()) - Running the hourly IMC script..."
        & $pythonInterpreterPath $hourlyScriptPath_IMC  # Run the hourly IMC script
        Write-Host "$($currentTime.ToString()) - Hourly IMC script completed."
    
        $lastHourlyRun_IMC = $currentTime  # Update the last run time for IMC script
        $nextHourlyRunTime_IMC = $lastHourlyRun_IMC.Date.AddHours($lastHourlyRun_IMC.Hour + 1).AddMinutes(30)
    }

    # Check if it's time to run the daily script
    if ($currentTime.Date -eq $lastDailyRun.Date.AddDays(1) -and $currentTime.TimeOfDay -ge [timespan]::FromHours(5)) {

        Write-Host "$($currentTime.ToString()) - Running the daily script..."
        & $pythonInterpreterPath $dailyScriptPath  # Run the daily script
        Write-Host "$($currentTime.ToString()) - Daily script completed."
    
        $lastDailyRun = [datetime]::Today.AddHours(5)  # Update the last daily run time
    }

    # Check if it's time to run the monthly script
    if ($currentTime -ge $nextMonthlyRunTime -and $currentTime.Day -eq 1 -and $currentTime.Hour -eq 7) {

        Write-Host "$($currentTime.ToString()) - Running the monthly script..."
        & $pythonInterpreterPath $monthlyScriptPath  # Run the monthly script
        Write-Host "$($currentTime.ToString()) - Monthly script completed."
    
        $lastMonthlyRun = $currentTime  # Update the last run time
        $nextMonthlyRunTime = $lastMonthlyRun.AddMonths(1) # Schedule the next monthly run
    }

    # Check if it's time to run the verbatim noon script
    if ($currentLondonTime -ge $nextRunTimeNoon) {
        
        Write-Host "$($currentTime.ToString()) - Running the verbatim script (Noon)..."
        & $pythonInterpreterPath $verbatimScriptPath  # Run the verbatim script
        Write-Host "$($currentTime.ToString()) - Verbatim script (Noon) completed."
    
        $nextRunTimeNoon = [datetime]::Today.AddHours(12).AddDays(1) # Schedule next run at noon
    }

    # Check if it's time to run the verbatim midnight script
    if ($currentLondonTime -ge $nextRunTimeMidnight) {
        
        Write-Host "$($currentTime.ToString()) - Running the verbatim script (Midnight)..."
        & $pythonInterpreterPath $verbatimScriptPath  # Run the verbatim script
        Write-Host "$($currentTime.ToString()) - Verbatim script (Midnight) completed."
    
        $nextRunTimeMidnight = [datetime]::Today.AddHours(24) # Schedule next run at midnight
    }
    
    Start-Sleep -Seconds 30 # Sleep for a while before checking again
}
