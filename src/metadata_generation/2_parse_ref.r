library(Rsubread)
library(sva)
library(ballgown)

REF_VERSION <- "Homo_sapiens.GRCh38.103"
REF_DATA_DIR <- file.path(getwd(), "data/reference")
GTF_FILE_NAME <- paste0(REF_VERSION, ".gtf.gz")
GENE_ANNOTATION_GTF <- file.path(REF_DATA_DIR, GTF_FILE_NAME)
PROCESSED_ANNOT_FILE_NAME <- paste0(REF_VERSION, ".allium.annotations.full.csv")
PROCESSED_ANNOT_PATH <- file.path(REF_DATA_DIR, PROCESSED_ANNOT_FILE_NAME)

cat("Gene annotation path:", GENE_ANNOTATION_GTF, "\n")

SAF <- Rsubread::flattenGTF(GENE_ANNOTATION_GTF)
GeneLength <- rowsum(SAF$End-SAF$Start+1, SAF$GeneID)
annot <- gffRead(GENE_ANNOTATION_GTF)

# Retrieve the attributes
annot$gene_id = getAttributeField(annot$attributes,
    field = "gene_id")

annot$gene_name = getAttributeField(annot$attributes,
    field = "gene_name")

annot$gene_biotype = getAttributeField(annot$attributes,
    field = "gene_biotype")

tokeep <- c("seqname", "feature", "gene_id", "gene_name", "gene_biotype")
annot_filtered <- annot[tokeep]

# Remove quotes
annot_filtered[] <- lapply(annot_filtered, gsub, pattern='"', replacement='')

# Keep only genes
annot_filtered <- annot_filtered[annot_filtered$feature == 'gene', ]

# Convert gene lengths to dataframe
gene_lengths <- as.data.frame(GeneLength)
gene_lengths$gene_id <- rownames(GeneLength)

# Reorder columns to have gene_id as the first column
gene_lengths <- gene_lengths[, c("gene_id", names(gene_lengths)[-ncol(gene_lengths)])]

# Name the columns
colnames(gene_lengths) <- c("gene_id", "gene_length")

# Join DataFrames on 'gene_id' column
full_annot <- merge(annot_filtered, gene_lengths, by = "gene_id", all = TRUE)

# Rename columns
colnames(full_annot) <- c("id", "chr", "feature", "name", "biotype", "length")

# Drop feature column
full_annot$feature <- NULL

# Strip trailing semicolons from the biotype column
full_annot$biotype <- sub(";$", "", full_annot$biotype)

# Sort annotations by id
full_annot <- full_annot[order(full_annot$id), ]

# Write processed metadata
write.table(full_annot, PROCESSED_ANNOT_PATH, col.names = TRUE, row.names = FALSE, sep = ',', quote = FALSE)
