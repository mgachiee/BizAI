export default function ButtonOptions({ index, handleButtons }) {
  const options = [
    ['Yes, proceed with business health check.', 'No, I\'m good.'],
    ['Yes, proceed with loaning application.', 'No, I\'m good.'],
  ];

  return (
    <div className="options-wrapper">
      {index !== undefined &&
        options[index].map((option, index) => {
          return (
            <div key={index} className="option yes-no-option" onClick={() => handleButtons(option)} >
              <p className="text-ellipsis overflow-hidden">{option}</p>
            </div>
          );
        })
      }
    </div>
  );
}