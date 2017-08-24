public class CodingBat {

  // RECURSION I //
  public int countPairs(String str) {
    if (str.length() <= 2) {
      return 0;
    } else if (str.charAt(0) == str.charAt(2)) {
      return 1 + countPairs(str.substring(1));
    } else {
      return countPairs(str.substring(1);
    }
  }

  public int countHi2(String str) {
    if (str.length() == 1 || str.length() == 0) {
      return 0;
    } else if (str.charAt(0) == 'x') {
      if (str.charAt(1) == 'h' && str.charAt(2) == 'i') {
        return countHi2(str.substring(2));
      } else {
        return countHi2(str.substring(1));
      }
    } else if (str.charAt(0) == 'h' && str.charAt(1) == 'i') {
      return 1 + countHi2(str.substring(1));
    } else {
      return countHi2(str.substring(1));
    }
  }

  public int countAbc(String str) {
    if (str.length() == 0 || str.length() == 1 || str.length() == 2) {
      return 0;
    } else if (str.charAt(0) == 'a' && str.charAt(1) == 'b' && (str.charAt(2) == 'c' || str.charAt(2) == 'a')) {
      return 1 + countAbc(str.substring(1));
    } else {
      return countAbc(str.substring(1));
    }
  }

  public String parenBit(String str) {
    int a = str.length();
    if (a <= 1) {
        return "";
    }
    if (str.substring(a - 1).equals(")")) {
      int paren = str.indexOf("(");
      return str.substring(paren);
    }
    return parenBit(str.substring(0,a - 1));
  }

  public int strCount(String str, String sub) {
    int a = str.length();
    int b = sub.length();
    if (a < b || b == 0){
      return 0;
    }
    if (str.substring(a - b).equals(sub)) {
      return 1 + strCount(str.substring(0,a - b),sub);
    }
    return strCount(str.substring(0,a - 1), sub);
  }

  // RECURSION II //
  public boolean splitArray(int[] nums) {
    return splitArrayAux(nums, 0, 0, 0);
  }
  public boolean splitArrayAux(int [] nums, int start, int first, int second) {
    if (start == nums.length) {
      return first == second;
    } else {
      return splitArrayAux(nums, start + 1, first + nums[start], second)
      || splitArrayAux(nums, start + 1, first, second + nums[start]);
    }
  }

  public boolean splitOdd10(int[] nums) {
    return splitOdd10Aux(nums, 0, 0, 0);
  }
  public boolean splitOdd10Aux(int [] nums, int start, int first, int second) {
    if (start == nums.length) {
      return (first % 10 == 0) && (second % 2 != 0);
    } else {
      return splitOdd10Aux(nums, start + 1, first + nums[start], second) ||
      splitOdd10Aux(nums, start + 1, first, second + nums[start]);
    }
  }

  public boolean groupSumClump(int start, int[] nums, int target) {
    if (start >= nums.length)
      return target == 0;
    int sum = 0;
    int i;
    for (i = start; i < nums.length; i++) {
      if (nums[i] == nums[start])
        sum += nums[start];
      else
        break;
    }
    return groupSumClump(i, nums, target - sum)
    || groupSumClump(i, nums, target);
  }

  public boolean groupSum5(int start, int[] nums, int target) {
    if (start == nums.length) {
      return target == 0;
    } else {
      if (nums[start] % 5 == 0) {
        return groupSum5(start + 1, nums, target - nums[start]);
      } else if (start > 0 && nums[start] == 1 && nums[start - 1] % 5 == 0) {
        return groupSum5(start + 1, nums, target);
      } else {
        return groupSum5(start + 1, nums, target - nums[start])
        || groupSum5(start + 1, nums, target);
      }
    }
  }

  public boolean split53(int[] nums) {
    return split53Aux(nums, 0, 0, 0);
  }
  public boolean split53Aux(int [] nums, int start, int first, int second) {
    if (start == nums.length) {
      return first == second;
    } else {
      if (nums[start] % 5 == 0) {
        return split53Aux(nums, start + 1, first + nums[start], second);
      } else if (nums[start] % 3 == 0) {
        return split53Aux(nums, start + 1, first, second + nums[start]);
      } else {
        return split53Aux(nums, start + 1, first + nums[start], second)
        || split53Aux(nums, start + 1, first, second + nums[start]);
      }
    }
  }
}
