# distillation_profile_calculation

This program is used to calculate the distillation profile for mixture of two crude oil.

Usage Syntax:

python main.py --crudeone <symbol for crude> --crudetwo <symbol for crude> --outfile <path to outputfile>

Example:

```
python main.py --crudeone "BCL" --crudetwo "MBL" --outfile distillation_profile.csv
```

Assumptions:
1) Assumed that the crude is always represented by the symbol provided in crudemonitor website. Ex: "BCL" for BC Light sour crude.
2) This program always uses the latest distillation profile as base/snapshot for the provided crude in the input.
3) 