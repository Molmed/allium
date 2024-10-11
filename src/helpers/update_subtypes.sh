# In specified file, replace old subtypes with new subtypes
# Usage: update_subtypes.sh <file>

if [ $# -ne 1 ]; then
    echo "Usage: update_subtypes.sh <file>"
    exit 1
fi

file=$1

sed -i 's/HeH/hyperdiploid/g' $file
sed -i 's/Hypo/hypodiploid/g' $file
sed -i 's/t(9;22)/BCR::ABL/g' $file
sed -i 's/ph-like/BCR::ABL-like/g' $file
sed -i 's/t(12;21)/ETV6::RUNX1/g' $file # Takes care of the likes as well
sed -i 's/11q23\/MLL/KMT2A-r/g' $file
sed -i 's/t(1;19)/TCF3::PBX1/g' $file
sed -i 's/PAX5 p.Pro80Arg/PAX5 P80R/g' $file
