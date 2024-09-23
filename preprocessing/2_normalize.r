library(edgeR)
library(sva)

# CHANGE THIS TO YOUR OWN GEX DATA
PATH_TO_GEX <- '/Users/marly389/Data/lilljebjorn/counts.filtered.lilljebjorn.csv'
OUTPUT_FILE_PATH <- '/Users/marly389/Data/lilljebjorn/counts.norm.lilljebjorn.csv'

REF_VERSION <- "Homo_sapiens.GRCh38.103"
REF_DATA_DIR <- file.path(getwd(), "data/reference")
PROCESSED_ANNOT_FILE_NAME <- paste0(REF_VERSION, ".allium.annotations.filtered.csv")
PROCESSED_ANNOT_PATH <- file.path(REF_DATA_DIR, PROCESSED_ANNOT_FILE_NAME)

# Read in data
x <- read.csv(PATH_TO_GEX, row.names = 1, header= TRUE, check.names = FALSE)
annot <- read.csv(PROCESSED_ANNOT_PATH, row.names = 1, header= TRUE, check.names = FALSE)

# Normalize for gene length in Kb
x_length_norm <- ( (x*10^3 )/annot$length)
d <- DGEList(counts=x_length_norm)
TMM <- calcNormFactors(d, method="TMM")
CPM <- cpm(TMM, log = TRUE)

# Write to file
write.csv(CPM, OUTPUT_FILE_PATH)
