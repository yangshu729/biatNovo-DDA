# change the old deepnovo data to new format
import csv
import re
from dataclasses import dataclass
import argparse


@dataclass
class Feature:
    spec_id: str
    mz: str
    z: str
    rt_mean: str
    seq: str
    scan: str

    def to_list(self):
        return [self.spec_id, self.mz, self.z, self.rt_mean, self.seq, self.scan, "0.0:1.0", "1.0"]


def transfer_mgf(old_mgf_file_name, output_feature_file_name, spectrum_fw=None):
    with open(old_mgf_file_name, "r") as fr:
        with open(output_feature_file_name, "w") as fw:
            writer = csv.writer(fw, delimiter=",")
            header = ["spec_group_id", "m/z", "z", "rt_mean", "seq", "scans", "profile", "feature area"]
            writer.writerow(header)
            flag = False
            for line in fr:
                if "BEGIN ION" in line:
                    flag = True
                    spectrum_fw.write(line)
                elif not flag:
                    spectrum_fw.write(line)
                elif line.startswith("TITLE="):
                    spectrum_fw.write(line)
                elif line.startswith("PEPMASS="):
                    mz = re.split("=|\r|\n", line)[1]
                    spectrum_fw.write(line)
                elif line.startswith("CHARGE="):
                    z = re.split("=|\r|\n|\+", line)[1]
                    spectrum_fw.write("CHARGE=" + z + "\n")
                elif line.startswith("SCANS="):
                    scan = re.split("=|\r|\n", line)[1]
                    spectrum_fw.write(line)
                elif line.startswith("RTINSECONDS="):
                    rt_mean = re.split("=|\r|\n", line)[1]
                    spectrum_fw.write(line)
                elif line.startswith("SEQ="):
                    seq = re.split("=|\r|\n", line)[1]
                elif line.startswith("END IONS"):
                    feature = Feature(spec_id=scan, mz=mz, z=z, rt_mean=rt_mean, seq=seq, scan=scan)
                    writer.writerow(feature.to_list())
                    flag = False
                    del scan
                    del mz
                    del z
                    del rt_mean
                    del seq
                    spectrum_fw.write(line)
                else:
                    spectrum_fw.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # ==============================================================================
    # FLAGS (options) for train
    # ==============================================================================
    parser.add_argument("--data_convert", action="store_true", default=False, help="Set to True for converting data.")
    parser.add_argument("--denovo_file", type=str, default="", help=".mgf file")
    parser.add_argument("--folder_name", type=str, default="", help="output folder name")
    opt = parser.parse_args()
    folder_name = opt.folder_name
    denovo_file = opt.denovo_file
    denovo_mgf_file = folder_name + "/" + "spectrum.mgf"
    denovo_output_feature_file = folder_name + "/" + "feature.test.csv"
    denovo_spectrum_fw = open(denovo_mgf_file, "w")
    transfer_mgf(denovo_file, denovo_output_feature_file, denovo_spectrum_fw)
    denovo_spectrum_fw.close()
