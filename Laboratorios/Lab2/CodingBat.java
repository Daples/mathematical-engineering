public class CodingBat {

  // Array II

  public int[] zeroFront(int[] nums) {
    boolean [] used = new boolean [nums.length];
    int cont = 0;
    for (int i = 0; i < nums.length; i++) {
      if(nums[i] == 0) {
        if (i != cont) {
          nums[i] = nums[cont];
          nums[cont] = 0;
        }
        cont++;
      }
    }
    return nums;
  }

  public int[] notAlone(int[] nums, int val) {
    for(int i = 1; i < nums.length-1; i++) {
      if(nums[i] == val && nums[i-1] != val && nums[i+1] != val) {
        if (nums[i-1] > nums[i+1])
          nums[i] = nums[i-1];
        else
          nums[i] = nums[i+1];
      }
    }
    return nums;
  }

  public boolean tripleUp(int[] nums) {
    for (int i = 0; i < nums.length - 2; i++) {
      if(nums[i] + 1 == nums[i+1] && nums[i] + 2 == nums[i+2]) return true;
    }
    return false;
  }

  public int[] tenRun(int[] nums) {
    int tempMult = 0;
    boolean used = false;
    for(int i = 0; i < nums.length; i++) {
      if (nums[i]%10 == 0) {
        used = true;
        tempMult = nums[i];
      }
      if(used)
        nums[i] = tempMult;
    }
    return nums;
  }

  public int[] shiftLeft(int[] nums) {
    int [] mod = new int[nums.length];
    if (nums.length==1) return nums;
    for (int i=1; i<nums.length; i++) {
      mod[nums.length-1]=nums[0];
      mod[i-1]=nums[i];
    }
    return mod;
  }

  // Array III

  public int[] seriesUp(int n) {
    int no = n*(n+1)/2;
    int [] nums = new int [no];
    int a = 0;
    for (int i = 1; i <= n; i++) {
      for (int j = 1; j <= i; j++) {
        nums[a] = j;
        a++;
      }
    }
    return nums;
  }

  public int countClumps(int[] nums) {
    int c = 0;
    for (int i = 0; i < nums.length-1; i++) {
      if (nums[i] == nums[i+1]) {
        for (int j = i; j < nums.length; j++) {
          if (nums[j] != nums[i]) {
            i = j;
            c++;
          }
          if (c == 0 && j == nums.length-1) {
            c++;
          }
        }
      }
    }
    return c;
  }

  public int[] squareUp(int n) {
    int [] nums = new int [n*n];
    int var = n;
    for (int i = n*n - 1; i >= 0; i -= n) {
      for (int j = 0; j < var; j++) {
        nums[i-j] = j + 1;
      }
      var--;
    }
    return nums;
  }

  public boolean linearIn(int[] outer, int[] inner) {
    int j = 0;
    int c = 0;
    if (inner.length == 0) {
      return true;
    }
    for (int i = 0; i < outer.length; i++) {
      if (inner[j] == outer[i]) {
        j++;
        if (j==inner.length) {
          return true;
        }
      }
    }
    return false;
  }

  public int[] fix45(int[] nums) {
    boolean [] arr = new boolean[nums.length];
    for (int i = 0; i < nums.length-1; i++) {
      if (nums[i] == 4 && nums[i+1] == 5) {
        arr[i+1] = true;
      } else  if (nums[i] == 4 && nums[i+1] != 5) {
        for (int j = 0; j < nums.length; j++) {
          if (nums[j] == 5 && arr[j] == false) {
            nums[j] = nums[i+1];
            nums[i+1] = 5;
            arr[i+1] = true;
            break;
          }
        }
      }
    }
    return nums;
  }
}
