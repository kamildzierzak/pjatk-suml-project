const Spinner = () => {
  return (
    <div className={`flex min-h-[512px] w-full items-center justify-center`}>
      <div
        className={`h-10 w-10 animate-spin rounded-full border-4 border-solid border-blue-500 border-t-transparent`}
      ></div>
    </div>
  );
};

export default Spinner;
