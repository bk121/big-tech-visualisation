import React, { useContext } from "react";
import { HiPlusCircle, HiMinusCircle } from "react-icons/hi";
import FilterElement from "./FilterElement";
import { GraphContext } from "../../../App";
import s from "./style.module.scss";

var othersExcluded = false;

export default function Filter() {
  const { nodeHook, linkHook, loadingHook, graphHook, styleHook, dateHook } =
    useContext(GraphContext);
  const { currentNodeTypes, setCurrentNodeTypes } = nodeHook;
  const { currentLinkTypes, setCurrentLinkTypes } = linkHook;
  const { graphLoading, setGraphLoading } = loadingHook;
  const { graph } = graphHook;
  const { nodeStyles } = styleHook;
  const { dateState, setDateState } = dateHook;

  // Turn array into format compatible with React-Select options
  const reactSelectFormatter = (array) => {
    return array.map((element) => ({
      value: `${element}`,
      label: `${element}`,
    }));
  };

  const nodeOptions = reactSelectFormatter(
    Array.from(new Set(graph.nodes.map((node) => node.label)))
  );
  const exclude = [
    "Name",
    "Owners",
    "Subsidiaries",
    "Founders",
    "Board_members",
  ];
  const otherSelectOption = reactSelectFormatter(["Other"])[0];
  const linkOptions = reactSelectFormatter(
    Array.from(
      new Set(
        graph.links
          .filter((link) => !exclude.includes(link.relationship))
          .map((link) => link.relationship)
      )
    ).concat(otherSelectOption.value)
  );

  const handleNodeChange = async (e) => {
    setGraphLoading(true);
    await setCurrentNodeTypes(e);
  };

  const handleLinkChange = async (e) => {
    let modifiedEvent = e.filter((el) => el.value !== otherSelectOption.value);
    othersExcluded = true;
    for (const obj of e) {
      if (obj.value === otherSelectOption.value) {
        othersExcluded = false;
        break;
      }
    }
    setGraphLoading(true);
    if (othersExcluded) {
      setCurrentLinkTypes(modifiedEvent);
    } else {
      setCurrentLinkTypes(reactSelectFormatter(exclude).concat(modifiedEvent));
    }
  };

  const handleClick = () => {
    if (dateState < 1) {
      setDateState(1);
    }
    setGraphLoading(false);
  };

  const nodeOptionStyles = {
    multiValue: (styles) => {
      return {
        ...styles,
        borderRadius: "100px",
        backgroundColor: "transparent",
        color: "white",
      };
    },
    multiValueLabel: (styles, node) => {
      return {
        ...styles,
        borderRadius: "100px",
        backgroundColor: nodeStyles[node.data.label],
        color: "white",
        border: "1px solid white",
      };
    },
    multiValueRemove: (styles) => {
      return {
        ...styles,
        backgroundColor: "transparent",
        color: "lightgrey",
        padding: "0px",
        ":hover": {
          cursor: "pointer",
        },
      };
    },
  };

  const linkOptionStyles = {
    multiValue: (styles) => {
      return {
        ...styles,
        color: "black",
      };
    },
  };

  const handleDateChange = async (e) => {
    setGraphLoading(true);
    if (parseInt(e.target.value) || e.target.value === "0") {
      setDateState(parseInt(e.target.value));
    } else {
      setDateState("");
    }
  };

  const handleDateDecrement = async (e) => {
    setGraphLoading(true);
    if (dateState && dateState > 1) {
      setDateState(parseInt(dateState) - 1);
    } else {
      setDateState(1);
    }
  };

  const handleDateIncrement = async (e) => {
    setGraphLoading(true);
    if (dateState) {
      setDateState(parseInt(dateState) + 1);
    } else {
      setDateState(1);
    }
  };

  return (
    <div className={s.container}>
      <FilterElement
        options={nodeOptions}
        placeholder={"Select node types..."}
        defaultValue={currentNodeTypes}
        handleChange={handleNodeChange}
        style={nodeOptionStyles}
        label={"Node Types"}
      />
      <FilterElement
        options={linkOptions}
        placeholder={"Select relationship types..."}
        defaultValue={currentLinkTypes
          .filter((link) => {
            return exclude.includes(link.value) === false;
          })
          .concat(othersExcluded ? undefined : otherSelectOption)}
        style={linkOptionStyles}
        handleChange={handleLinkChange}
        label={"Relationship Types"}
      />
      <div className={s.dateRangeContainer}>
        <h5 style={{ marginTop: "30px" }}>Days Since Publishing</h5>
        <form autoComplete="off">
          <div className={s.inputStyles}>
            <HiMinusCircle
              style={{
                color: "#fff",
                backgroundColor: "#2090ff",
                border: "none",
                marginRight: "10px",
                borderRadius: "100px",
                fontSize: "30px",
                cursor: "pointer",
              }}
              onClick={handleDateDecrement}
            />
            <input
              style={{
                width: "100px",
                textAlign: "center",
              }}
              value={dateState}
              onChange={handleDateChange}
            />
            <HiPlusCircle
              style={{
                color: "#fff",
                backgroundColor: "#2090ff",
                border: "none",
                marginLeft: "10px",
                borderRadius: "100px",
                fontSize: "30px",
                cursor: "pointer",
              }}
              onClick={handleDateIncrement}
            />
          </div>
        </form>
      </div>
      <div
        onClick={graphLoading ? handleClick : undefined}
        className={graphLoading ? s.buttonStyle : s.inactiveButtonStyle}
      >
        Apply
      </div>
    </div>
  );
}
