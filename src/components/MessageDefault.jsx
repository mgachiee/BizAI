/*
  Author: Mark Allen G. Bobadilla
  Date: November 2024
  Github: mgachiee
*/

import { DEFAULT_OPTIONS } from "../util";

export default function MessageDefault({ handleButtons }) {
  // handles the default options (startup look) of the app
  return (
    <div className="options-wrapper">
      {DEFAULT_OPTIONS.map((option, index) => {
        return (
          <div key={index} className="option" onClick={() => handleButtons(option)} >
            <p>{option}</p>
          </div>
        );
      })}
    </div>
  );
}