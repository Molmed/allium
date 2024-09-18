library(Rsubread)
library(sva)
library(ballgown)

# Function to get the directory of the current script
get_script_dir <- function() {
  cmdArgs <- commandArgs(trailingOnly = FALSE)
  match <- grep("--file=", cmdArgs)
  if (length(match) > 0) {
    return(dirname(normalizePath(sub("--file=", "", cmdArgs[match]))))
  } else {
    return(dirname(normalizePath(sys.frames()[[1]]$ofile)))
  }
}

# Define a constant REF_GENOME relative to the script's directory
script_dir <- get_script_dir()
REF_GENOME <- file.path(script_dir, "../../data/reference/Homo_sapiens.GRCh38.103.gtf")

# Print the constant REF_GENOME
cat("Reference Genome Path:", REF_GENOME, "\n")
