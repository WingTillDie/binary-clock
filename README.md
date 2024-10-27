# binary-clock
Binary clock with 32:64:64 time format, with quadrant symbols

## Description
Available output time formats: 24:60:60 time format, 32:64:64 time format  
Available output symbol formats: decimal, binary, binary with quadrant symbol  
The program is a real application to demonstrate that using quadrant symbol to repesent binary numbers can improve legibility  


## Example Outputs
```
binary-clock$ ./binary-clock.py
20:04:00 10100:000100:000000 ◳◱◳◱◱:◱◱◱◳◱◱:◱◱◱◱◱◱ 26:04:00 11010:000100:000000 ◳◳◱◳◱:◱◱◱◳◱◱:◱◱◱◱◱◱
```

![screenshot](image.png)

## Program Flow Chart
```mermaid
flowchart TD
    main --> get_current_time
    get_current_time -->|HH:MM:DD| time_to_quadrants
    subgraph time_to_quadrants
        num_to_quadrants -->|number| num_to_bins -->|several binary digits| bins_to_quadrants -->|a binary digit| bin_to_quadrant -->|a quadrant symbol| return_time_to_quadrants
    end
    main --> get_current_time_fractions
    get_current_time -->|HH:MM:DD| time_to_bin_encoding_to_quadrants
    get_current_time_fractions -->|h_fraction,<br>m_fraction,<br>s_fraction | time_to_bin_encoding_to_quadrants
    subgraph time_to_bin_encoding_to_quadrants
        time_to_bin_encoding_to_bins -->|number| clog2 -->|number of digits of binary| float_to_bin -->|binary number| return_time_to_bin_encoding_to_quadrants
    end
```

## Program Call Graph
```mermaid
graph TD
    main --> num_args{num_args}
    num_args -->|0| clock
    num_args -->|1| num_to_quadrants
    clock --> 24:60:60[24:60:60 time format]
    24:60:60 --> get_current_time & time_to_bins & time_to_quadrants
    time_to_quadrants -->|number| num_to_quadrants
    num_to_quadrants -->|number| num_to_bins
    num_to_quadrants -->|several binary digits| bins_to_quadrants
    bins_to_quadrants -->|a bindary digit| bin_to_quadrant
    time_to_bins --> num_to_bins

    clock --> 32:64:64[32:64:64 time format]
    32:64:64 --> get_current_time_fractions & time_to_bin_encoding & time_to_bin_encoding_to_bins & time_to_bin_encoding_to_quadrants
    time_to_bin_encoding & time_to_bin_encoding_to_quadrants --> time_to_bin_encoding_to_bins

    time_to_bin_encoding_to_bins --> time_to_bin_encoding_to_bins_wo_advancement & time_to_bin_encoding_to_bins_w_advancement

    time_to_bin_encoding_to_bins_wo_advancement --> is_w_fractions{is_w_fractions}
    is_w_fractions -->|False| time_to_bin_encoding_to_bins_wo_fractions
    is_w_fractions -->|True| time_to_bin_encoding_to_bins_w_fractions

    time_to_bin_encoding_to_bins_wo_advancement & time_to_bin_encoding_to_bins_w_advancement --> time_to_bin_encoding_to_bins_wo_or_w_advancement((" "))

    time_to_bin_encoding_to_bins_wo_or_w_advancement --> float_to_bin & clog2
```

