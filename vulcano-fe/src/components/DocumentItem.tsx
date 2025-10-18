import React from "react";
import '../styles/main.scss';
import EyeIcon from "../assets/eye.png";
import DownloadIcon from "../assets/download.png";
import FileIcon from "../assets/file.png";
import QuestionMarkIcon from "../assets/question-mark.png";

type DocumentItemType = "file" | "answer";

interface DocumentItemProps {
  name: string;
  selected?: boolean;
  type?: DocumentItemType;
  onView?: () => void;
  onDownload?: () => void;
}

const DocumentItem: React.FC<DocumentItemProps> = ({
  name,
  type = "file",
  selected = false,
  onView,
  onDownload
}) => {
  return (
    <div className={`file-view ${selected ? "selected" : ""}`}>
      <div
        className="file-icon cursor-pointer"
        onClick={onView}>
        <img
          src={type === "answer" ? QuestionMarkIcon : FileIcon}
          alt={type === "answer" ? "Answer" : "File"}
        />
      </div>

      <div
        className={`file-name${onView ? " cursor-pointer" : ""}`}
        onClick={onView}>
        {name}
      </div>

      {type === "file" && (
        <div className="file-actions">
          <button className="view-btn" onClick={onView}>
            <img src={EyeIcon} alt="View" />
          </button>
          <button className="download-btn" onClick={onDownload}>
            <img src={DownloadIcon} alt="Download" />
          </button>
        </div>
      )}
    </div>
  );
};

export default DocumentItem;
